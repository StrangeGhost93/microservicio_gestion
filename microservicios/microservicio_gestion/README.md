# Microservicio de Especialidades (Flask + Postgres)

Catálogo de especialidades respaldado por Postgres con Flask + SQLAlchemy. Expone `/api/v1/especialidades` (listado) y `/api/v1/especialidades/<id>` (detalle), más healthcheck.

## Stack

| Capa | Tecnología |
| ---- | ---------- |
| Framework | Flask 3 + Blueprints |
| Persistencia | Postgres (SQLAlchemy + Flask-Migrate) |
| Contenedor | Python 3.11 slim + Gunicorn |

## Dependencias

- Se gestionan con `pyproject.toml` (sin `requirements.txt`).
- Opción simple (pip):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install flask==3.0.2 flask-sqlalchemy==3.1.1 flask-migrate==4.0.7 python-dotenv==1.0.1 requests==2.32.3 pytest==9.0.2 psycopg2-binary==2.9.9
   ```
- Opción con `uv` (si lo tenés global):
   ```powershell
   python -m uv venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m uv sync
   ```

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
├── Dockerfile
└── README.md
```

## Configuración

1. Clonar el proyecto base y ubicarse en `microservicios/microservicio_gestion`.
2. Crear entorno virtual e instalar dependencias (pip):
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install flask==3.0.2 flask-sqlalchemy==3.1.1 flask-migrate==4.0.7 python-dotenv==1.0.1 requests==2.32.3 pytest==9.0.2
   ```
3. Duplicar `.env.example` como `.env` y completar `GESTION_SECRET_KEY` (lo usa Flask). Define también `FLASK_CONTEXT` (development/testing/production) y URIs de DB (`DEV/TEST/PROD_DATABASE_URI`).
4. Ejecutar migraciones y levantar el servicio:
   ```powershell
   flask db upgrade
   flask run --port 5002
   ```

### Variables de entorno clave

| Variable | Uso |
| -------- | --- |
| `FLASK_CONTEXT` | `development` / `testing` / `production` |
| `DEV/TEST/PROD_DATABASE_URI` | URIs por entorno (prefijo `GESTION_` en `.env` del docker compose) |
| `GESTION_SECRET_KEY` | Firmado de sesiones |
| `DOCUMENTACION_BASE_URL` | URL base para el microservicio de documentación |
| `DOCUMENTACION_TIMEOUT` | Timeout (s) para las consultas HTTP hacia documentación |

## Endpoints principales (`/api/v1`)

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| GET | `/status` | Healthcheck |
| GET | `/especialidades` | Catálogo de especialidades (DB) |
| GET | `/especialidades/<id>` | Detalle de una especialidad |

> Todos los cuerpos aceptan/retornan JSON y validan estructura mediante Marshmallow. Los listados soportan filtros opcionales (`vigente`, `programa`, `estado`, `especialidad`).

## Flujo típico

1. Crear DB y aplicar migraciones: `flask db upgrade` (usa el `FLASK_CONTEXT` actual).
2. Poblar datos iniciales (opcional) con seeds vía repositorio o comandos personalizados.
3. Consultar listados/detalles de especialidades desde `/api/v1/especialidades`.

## Extender el microservicio

- Agrega migraciones y seeds en `/migrations` utilizando Flask-Migrate.
- Suma autenticación (JWT u OIDC) envolviendo los blueprints con decoradores.
- Implementa reportes agregados en nuevos servicios/recursos.
- Añade pruebas unitarias en `tests/` aprovechando la configuración `TestingConfig`.

## Resiliencia operativa

- Persistencia en Postgres; la configuración apunta a SQLite por defecto en desarrollo si no se definen URIs.

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

- Usa Postgres en `docker-compose`; en local puede apuntar a SQLite si no configurás la URI.
- Healthcheck disponible en `GET /api/v1/status`.

## Principios de código limpio aplicados

- **Separación por capas**: Resources delegan en Services y éstos en Repositories.
- **Configuración controlada**: Variables en `.env` / `.env-example`, nunca hardcodeadas.
- **Pruebas**: Usa `TestingConfig` + SQLite en memoria para pruebas con `pytest`.
