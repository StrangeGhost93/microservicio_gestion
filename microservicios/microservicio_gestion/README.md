# Microservicio de Especialidades (mock)

Microservicio Flask reducido a un catálogo simulado de especialidades. No usa base de datos ni Redis; sólo expone un endpoint para listar especialidades y otro para obtener el detalle por ID, más el healthcheck.

## Stack

| Capa | Tecnología |
| ---- | ---------- |
| Framework | Flask 3 + Blueprints |
| Persistencia | No aplica (mock en memoria) |
| Contenedor | Python 3.11 slim + Gunicorn |

## Dependencias

- Se gestionan con `uv` y el `pyproject.toml` (no se usa `requirements.txt`).
- En local podés crear un entorno con `uv venv .venv` y activarlo; luego `uv pip install --system flask gunicorn` o `uv sync` si preferís.

## Estructura de carpetas

```
microservicios/microservicio_gestion/
├── app/
│   ├── __init__.py           # Factory y registro de extensiones
│   ├── config.py             # Configuración por entorno
│   ├── extensions.py         # SQLAlchemy, Marshmallow, cache, limiter
│   ├── models/               # Programa, Modulo, Cohorte, Docente, Asignacion
│   ├── repositories/         # Acceso a datos desacoplado
│   ├── services/             # Reglas de negocio y orquestación
│   ├── schemas/              # Validación/serialización de payloads
│   ├── resources/            # Endpoints Flask (Blueprints)
│   └── validators/           # Decoradores reutilizables
├── app.py                    # Punto de entrada
├── requirements.txt
├── Dockerfile
└── README.md
```

## Configuración

1. Clonar el proyecto base y ubicarse en `microservicios/microservicio_gestion`.
2. Crear entorno virtual e instalar dependencias:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Duplicar `.env.example` como `.env` y completar `GESTION_SECRET_KEY` (lo usa Flask).
4. Levantar el servicio:
   ```powershell
   flask run --port 5002
   ```

### Variables de entorno clave

| Variable | Uso |
| -------- | --- |
| `FLASK_ENV` | `development` / `production` |
| `GESTION_*_DATABASE_URI` | URIs por entorno |
| `GESTION_SECRET_KEY` | Firmado de sesiones JWT/CSRF |
| `GESTION_REDIS_URL` | Cache + rate limiting (ej. `redis://localhost:6379/0`) |
| `GESTION_RATE_LIMIT` | Límite por defecto de solicitudes (p. ej. `60 per minute`) |
| `DOCUMENTACION_BASE_URL` | URL base para el microservicio de documentación |
| `DOCUMENTACION_TIMEOUT` | Timeout (s) para las consultas HTTP hacia documentación |

## Endpoints principales (`/api/v1`)

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| GET | `/status` | Healthcheck |
| GET | `/especialidades` | Catálogo mock de especialidades |
| GET | `/especialidades/<id>` | Detalle mock de una especialidad |

> Todos los cuerpos aceptan/retornan JSON y validan estructura mediante Marshmallow. Los listados soportan filtros opcionales (`vigente`, `programa`, `estado`, `especialidad`).

## Flujo típico

1. **Crear programa** → `POST /programas`.
2. **Agregar módulos** → `POST /programas/<programaId>/modulos`.
3. **Planificar cohorte** → `POST /cohortes` indicando programa, campus y cupo.
4. **Registrar docentes** → `POST /docentes`.
5. **Asignar docentes** → `POST /cohortes/<cohorteId>/docentes` con `docente_id`, `modulo_id` y horas.

## Extender el microservicio

- Agrega migraciones y seeds en `/migrations` utilizando Flask-Migrate.
- Suma autenticación (JWT u OIDC) envolviendo los blueprints con decoradores.
- Implementa reportes agregados (horas planificadas por docente, ocupación de cohortes) en nuevos servicios/recursos.
- Añade pruebas unitarias en `tests/` aprovechando la configuración `TestingConfig`.

## Resiliencia operativa

- No depende de Redis ni base de datos. Los datos están embebidos en memoria.

## Pruebas

Recomendado: probar manualmente con `curl` o similar:

```powershell
curl http://localhost:5002/api/v1/status
curl http://localhost:5002/api/v1/especialidades
curl http://localhost:5002/api/v1/especialidades/1
```

## Docker

```
docker build -t gestion-ms .
docker run -p 5002:5000 --env-file .env gestion-ms
```

Esto levanta Gunicorn serveando `app:app` listo para integrarse via `docker-compose` junto al resto del ecosistema SYSACAD.

## Orquestación con el resto de los microservicios

El árbol raíz (`Desarrollo de software Parcial 2/`) incluye un `docker/docker-compose.yml` capaz de levantar esta API junto a `microservicio_alumno` y `microservicio_documentacion`. Requisitos:

1. Tener las carpetas hermanas clonadas:
   - `Desarrollo de software Parcial 2/microservicios/microservicio_gestion`
   - `../microservicio_alumno`
   - `../microservicio_documentacion`
2. Copiar los archivos de entorno y completar credenciales reales:
   ```powershell
   cd docker
   Copy-Item .env-example .env
   ```
3. Levantar la pila completa:
   ```powershell
   docker compose up --build gestion alumno documentacion
   ```
4. Ejecutar migraciones dentro de cada contenedor una sola vez:
   ```powershell
   docker compose exec gestion flask db upgrade
   docker compose exec alumno python manage.py migrate
   docker compose exec documentacion flask db upgrade
   ```

| Servicio                | Puerto expuesto | Uso principal                                   |
|-------------------------|-----------------|--------------------------------------------------|
| `gestion`               | 5002 → 5000     | Programas, módulos, cohortes y docentes          |
| `documentacion`         | 5001 → 5000     | Generación de certificados y documentos oficiales|
| `alumno`                | 8000 → 8000     | Gestión de alumnos, planes y entidades académicas|
| `estructura` (monolito) | 5000 → 5000     | API histórica SYSACAD                            |

Todos los servicios comparten la red `sysacad_net`, por lo que pueden comunicarse mediante hostnames (`http://gestion:5000/api/v1/programas`, `http://documentacion:5000/api/v1/certificados`, etc.).

### Interacciones comunes

- Este microservicio ahora sólo entrega datos mock de especialidades. Útil para pruebas de front o integración simple.
- Healthcheck disponible en `GET /api/v1/status`.

## Principios de código limpio aplicados

- **Separación por capas**: Resources delegan en Services y éstos en Repositories; no mezclamos acceso a `request`, reglas de negocio y persistencia.
- **Validaciones explícitas**: Todo payload pasa por `Marshmallow` + `validate_with`, evitando lógica defensiva repetida.
- **Tipado y docstrings**: Los módulos incluyen anotaciones (`Mapping`, `Sequence`) y descripciones breves. Consulta `docs/CLEAN_CODE.md` para el checklist completo adoptado por el proyecto.
- **Configuración controlada**: Variables en `.env` / `.env-example`, nunca hardcodeadas. Los valores compartidos (URIs, límites, secretos) viven en un solo archivo.
- **Pruebas**: Prepara casos unitarios en `tests/` utilizando la `TestingConfig`. Antes de mergear corré `pytest` (o `python -m pytest`) y, si es relevante, `docker compose up --build` para validar la integración cruzada.
