# Microservicio de Gestión Académica

Microservicio Flask responsable de la gestión académica (programas, módulos, cohortes y asignaciones docentes) dentro del ecosistema SYSACAD. Trabaja en conjunto con `microservicio_alumno` (alta/baja de estudiantes) y `microservicio_documentacion` (certificados y documentación oficial) exponiendo APIs REST que los demás servicios consumen para saber **qué** se dicta, **cuándo** y **con quién**.

## Características principales

- CRUD de programas académicos con versionado, modalidad y estado de vigencia.
- Gestión de módulos (asignaturas cortas) asociados a cada programa.
- Administración de cohortes con campus/modalidad, cupos y estado de planificación.
- Registro de docentes externos e internos, con especialidad y disponibilidad.
- Asignación de docentes a módulos/cohortes con control de horas semanales.
- Identificadores públicos idénticos a los IDs reales para alinear los contratos con el resto de los servicios.
- Validación de payloads con Marshmallow + decorador `validate_with`.
- Arquitectura por capas (Resources → Services → Repositories → Models) lista para escalar.

## Stack

| Capa | Tecnología |
| ---- | ---------- |
| Framework | Flask 3 + Blueprints |
| Persistencia | SQLAlchemy + Flask-Migrate |
| Validación | Marshmallow |
| Contenedor | Python 3.11 slim + Gunicorn |

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
3. Duplicar `.env.example` como `.env` y actualizar credenciales/URIs.
4. Crear base y correr migraciones (una vez que agregues `flask db init/migrate`):
   ```powershell
   flask db upgrade
   ```
5. Levantar el servicio:
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
| GET/POST | `/programas` | Listar/crear programas |
| GET/PUT/DELETE | `/programas/<id>` | Obtener/editar/borrar programa |
| GET/POST | `/programas/<id>/modulos` | Listar o crear módulos de un programa |
| GET | `/cohortes?programa=<id>&estado=abierta` | Cohortes filtradas |
| POST | `/cohortes` | Crear nueva cohorte |
| POST | `/cohortes/<id>/docentes` | Asignar docente a módulo + cohorte |
| CRUD | `/docentes` | Alta/baja/modificación de docentes |
| GET | `/integraciones/documentacion/status` | Consulta resiliente al MS de documentación |

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

- **Caching + rate limiting**: El endpoint más consultado (`GET /api/v1/programas`) usa `Flask-Caching` respaldado en Redis y `Flask-Limiter`. Esto justifica la presencia de Redis aunque el microservicio gestione programas: la lista de planes académicos es la fuente más leída por el resto del ecosistema.
- **Integración observable**: `GET /api/v1/integraciones/documentacion/status` expone el estado del microservicio de Documentación sin aplicar circuit breaker propio; las políticas de reintento/aislamiento ya las maneja Traefik a nivel plataforma.
- **Configuración moldeable**: Los parámetros (Redis, límites, timeout del cliente externo) viven en el `.env` para ajustarlos por entorno sin tocar código.

## Pruebas automatizadas

El microservicio cuenta con una batería de pruebas `pytest` que cubre:

- Cliente HTTP hacia documentación ante respuestas exitosas y errores controlados.
- Endpoint de integraciones para propagar el estado remoto.
- Parsing de filtros y cacheo en `program_resource`.

Ejecución recomendada desde la raíz del repo:

```powershell
python -m pytest microservicios/microservicio_gestion/tests
```

La `TestingConfig` utiliza `SimpleCache` y un backend de rate limiting en memoria, por lo que no es necesario tener Redis corriendo para los tests unitarios.

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

- `microservicio_documentacion` consulta `GET /api/v1/programas` y `GET /api/v1/cohortes` para poblar certificados de cursado.
- `microservicio_alumno` utiliza `GET /api/v1/programas/<id>` para validar que el plan elegido por un estudiante existe y está vigente.
- Cualquier otro servicio puede verificar la salud de este microservicio accediendo a `GET /api/v1/status`.

## Principios de código limpio aplicados

- **Separación por capas**: Resources delegan en Services y éstos en Repositories; no mezclamos acceso a `request`, reglas de negocio y persistencia.
- **Validaciones explícitas**: Todo payload pasa por `Marshmallow` + `validate_with`, evitando lógica defensiva repetida.
- **Tipado y docstrings**: Los módulos incluyen anotaciones (`Mapping`, `Sequence`) y descripciones breves. Consulta `docs/CLEAN_CODE.md` para el checklist completo adoptado por el proyecto.
- **Configuración controlada**: Variables en `.env` / `.env-example`, nunca hardcodeadas. Los valores compartidos (URIs, límites, secretos) viven en un solo archivo.
- **Pruebas**: Prepara casos unitarios en `tests/` utilizando la `TestingConfig`. Antes de mergear corré `pytest` (o `python -m pytest`) y, si es relevante, `docker compose up --build` para validar la integración cruzada.
