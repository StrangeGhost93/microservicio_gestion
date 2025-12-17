# PROYECTO-SYSACAD

**Integrantes:** Juan Destéfano y Occhipinti Julián.

Este proyecto fue realizado con la ayuda de GitHub Copilot, ChatGPT y DeepSeek.

[Información Útil](https://cake-sushi-9a6.notion.site/Info-til-1c29afa16efd8055b44ddbd7f53260b8?pvs=4)

## 📋 Descripción del Proyecto
Sistema de gestión académica desarrollado en Python para la administración de facultades, materias, alumnos y certificados.

## ⚙️ Requerimientos Técnicos
- Python 3.8 o superior
- Dependencias con `uv` (ej.: `uv pip install -r requirements.txt`)
- Base de datos SQLite por defecto en local; el stack Docker usa PostgreSQL/Redis configurables por `.env`
- Docker (opcional para despliegue)

## 🚀 Cómo Ejecutar el Proyecto
1. Copiá las variables de ejemplo: `Copy-Item env-example .env`
2. Elegí el contexto (development | testing | production): `$Env:FLASK_CONTEXT = "development"`
3. Creá y activá el entorno virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Instalá dependencias con uv: `uv pip install -r requirements.txt`
5. Levantá la app monolito:
   ```powershell
   python app.py
   # o
   flask run --port 5000
   ```

## Instalación

1. Cloná el repositorio.

2. Creá un entorno virtual en la carpeta del proyecto:
   ```bash
   python -m venv env_name
   ```
   O bien, podés crearlo en una carpeta diferente *(sugerido)*:
   ```bash
   python -m venv C:\Users\userX\environments\gral_env
   ```

3. Activá el entorno virtual. Dependiendo de la terminal que uses, el comando varía:

   **Git Bash (Windows):**
   ```bash
   source env_name/Scripts/activate
   ```

   **CMD (Windows):**
   ```cmd
   env_name\Scripts\activate
   ```

   Una vez activado, deberías ver algo como `(env_name)` al inicio de la línea en tu terminal.  
   Si no lo ves, probá con:
   ```bash
   which python
   ```


4. Instalá las dependencias en el entorno virtual seleccionado:
   ```bash
   uv pip install -r requirements.txt
   ```

5. Ejecutá los tests para verificar que todo funciona correctamente:
   **Windows (PowerShell):**
   ```powershell
   & "env_name\Scripts\python.exe" -m unittest discover -s test
   ```
   O si el entorno ya está activado:
   ```powershell
   python -m unittest discover -s test
   ```

   **Linux / Mac / Git Bash:**
   ```bash
   source env_name/bin/activate
   python -m unittest discover -s test
   ```

## Ejecutar un test específico

**Windows (PowerShell):**
```powershell
& "env_name\Scripts\python.exe" -m unittest test.test_facultad
```
O si el entorno ya está activado:
```powershell
python -m unittest test.test_facultad
```

**Linux / Mac / Git Bash:**
```bash
source env_name/bin/activate
python -m unittest test.test_facultad
```

## 🧩 Microservicios del proyecto

### Gestión (especialidades con DB Postgres)
- Código en `microservicios/microservicio_gestion`, expone `/api/v1/especialidades` y `/api/v1/especialidades/<id>` más healthcheck.
- Dependencias gestionadas con `pyproject.toml`. Instalación rápida:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install flask==3.0.2 flask-sqlalchemy==3.1.1 flask-migrate==4.0.7 python-dotenv==1.0.1 requests==2.32.3 pytest==9.0.2 psycopg2-binary==2.9.9
   ```
   Con uv: `python -m uv venv .venv && .\.venv\Scripts\Activate.ps1 && python -m uv sync`.
- Ejecución local: `cd microservicios/microservicio_gestion`, copiar `.env.example` a `.env`, definir `FLASK_CONTEXT=development` y una `DEV_DATABASE_URI` (SQLite por defecto o Postgres). Luego `flask db upgrade` y `flask run --port 5002`.
- En Docker: `cd docker && cp .env-example .env && docker compose up gestion gestion-db` (requiere red `mired`). Para exponer al host, agrega `ports: - "5002:5000"` en el servicio `gestion`.

### Levantar todo el ecosistema (Alumno + Documentación + Gestión)

1. Creá la red compartida (mismo criterio que el repo de referencia):
   ```powershell
   docker network create mired
   ```

2. Asegurate de tener los tres repositorios clonados como carpetas hermanas:
   - `Desarrollo de software Parcial 2/` (este repo, contiene `docker/`)
   - `../microservicio_alumno/`
   - `../microservicio_documentacion/`
3. Desde `Desarrollo de software Parcial 2/docker/` copiá las variables ejemplo:
   ```powershell
   cd docker
   Copy-Item .env-example .env
   ```
   Editá `.env` con las credenciales reales de cada microservicio (PostgreSQL, Redis, claves secretas, etc.).
4. Construí y levantá los contenedores necesarios (la red `sysacad_net` ahora apunta a `mired`):
   ```powershell
   docker compose up --build gestion alumno documentacion
   ```
   Se expondrán los puertos: `estructura` 5000, `documentacion` 5001, `gestion` 5002 y `alumno` 8000.
5. Ejecutá las migraciones y seeds desde los contenedores (solo la primera vez):
   ```powershell
   docker compose exec gestion flask db upgrade
   docker compose exec alumno python manage.py migrate
   docker compose exec documentacion flask db upgrade
   docker compose exec documentacion python poblar_db.py   # Opcional, llena datos de ejemplo
   ```
6. Probá la comunicación entre microservicios usando las URLs internas (`http://gestion:5000`, `http://alumno:8000`, `http://documentacion:5000`) o los puertos publicados hacia tu host.
