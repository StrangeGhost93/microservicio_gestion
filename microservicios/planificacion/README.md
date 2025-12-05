# Microservicio de Planificación Académica

Servicio Flask pensado para centralizar la planificación anual de programas ejecutivos, módulos, cohortes y asignaciones docentes del ecosistema SYSACAD. Complementa a los microservicios existentes de alumnos/documentación enfocándose en **qué** se dicta, **cuándo** y **con quién**.

## Características principales

- CRUD de programas académicos con versionado, modalidad y estado de vigencia.
- Gestión de módulos (asignaturas cortas) asociados a cada programa.
- Administración de cohortes con campus/modalidad, cupos y estado de planificación.
- Registro de docentes externos e internos, con especialidad y disponibilidad.
- Asignación de docentes a módulos/cohortes con control de horas semanales.
- Identificadores ofuscados mediante Hashids en todas las rutas públicas.
- Validación de payloads con Marshmallow + decorador `validate_with`.
- Arquitectura por capas (Resources → Services → Repositories → Models) lista para escalar.

## Stack

| Capa | Tecnología |
| ---- | ---------- |
| Framework | Flask 3 + Blueprints |
| Persistencia | SQLAlchemy + Flask-Migrate |
| Validación | Marshmallow |
| Serialización IDs | Flask-Hashids |
| Contenedor | Python 3.11 slim + Gunicorn |

## Estructura de carpetas

```
microservicios/planificacion/
├── app/
│   ├── __init__.py           # Factory y registro de extensiones
│   ├── config.py             # Configuración por entorno
│   ├── extensions.py         # SQLAlchemy, Marshmallow, Hashids
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

1. Clonar el proyecto base y ubicarse en `microservicios/planificacion`.
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
| `PLANIFICACION_*_DATABASE_URI` | URIs por entorno |
| `PLANIFICACION_SECRET_KEY` | Firmado de sesiones JWT/CSRF |
| `HASHIDS_*` | Parámetros para ofuscar IDs |

## Endpoints principales (`/api/v1`)

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| GET | `/status` | Healthcheck |
| GET/POST | `/programas` | Listar/crear programas |
| GET/PUT/DELETE | `/programas/<hashid>` | Obtener/editar/borrar programa |
| GET/POST | `/programas/<hashid>/modulos` | Listar o crear módulos de un programa |
| GET | `/cohortes?programa=<hashid>&estado=abierta` | Cohortes filtradas |
| POST | `/cohortes` | Crear nueva cohorte |
| POST | `/cohortes/<hashid>/docentes` | Asignar docente a módulo + cohorte |
| CRUD | `/docentes` | Alta/baja/modificación de docentes |

> Todos los cuerpos aceptan/retornan JSON y validan estructura mediante Marshmallow. Los listados soportan filtros opcionales (`vigente`, `programa`, `estado`, `especialidad`).

## Flujo típico

1. **Crear programa** → `POST /programas`.
2. **Agregar módulos** → `POST /programas/<programaHashid>/modulos`.
3. **Planificar cohorte** → `POST /cohortes` indicando programa, campus y cupo.
4. **Registrar docentes** → `POST /docentes`.
5. **Asignar docentes** → `POST /cohortes/<cohorteHashid>/docentes` con `docente_hashid`, `modulo_hashid` y horas.

## Extender el microservicio

- Agrega migraciones y seeds en `/migrations` utilizando Flask-Migrate.
- Suma autenticación (JWT u OIDC) envolviendo los blueprints con decoradores.
- Implementa reportes agregados (horas planificadas por docente, ocupación de cohortes) en nuevos servicios/recursos.
- Añade pruebas unitarias en `tests/` aprovechando la configuración `TestingConfig`.

## Docker

```
docker build -t planificacion-ms .
docker run -p 5002:5000 --env-file .env planificacion-ms
```

Esto levanta Gunicorn serveando `app:app` listo para integrarse via `docker-compose` junto al resto del ecosistema SYSACAD.

## Integración en el monorepo

- Dentro del repositorio principal reside en `microservicios/planificacion` y se incluye en `docker/docker-compose.yml` como servicio `planificacion`.
- Podés levantarlo junto con los demás microservicios ejecutando `docker compose up planificacion` desde la carpeta `docker/` (o `docker compose up` para toda la pila).
- Todas las variables necesarias se documentan en los archivos `env-example` de la raíz y de `docker/`; copiá esos archivos a `.env` y completá tus credenciales antes de construir las imágenes.
