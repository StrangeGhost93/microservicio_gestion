# PROYECTO-SYSACAD

**Integrantes:** Juan Destéfano y Occhipinti Julián.

Este proyecto fue realizado con la ayuda de GitHub Copilot, ChatGPT y DeepSeek.

[Información Útil](https://cake-sushi-9a6.notion.site/Info-til-1c29afa16efd8055b44ddbd7f53260b8?pvs=4)

## 📋 Descripción del Proyecto
Sistema de gestión académica desarrollado en Python para la administración de facultades, materias, alumnos y certificados.

## ⚙️ Requerimientos Técnicos
- Python 3.8 o superior
- Dependencias: `pip install -r requirements.txt`
- Base de datos SQLite (incluida)
- Docker (opcional para despliegue)

## 🚀 Cómo Ejecutar el Proyecto

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
   pip install -r requirements.txt
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

### Gestión (mock de especialidades)
- El código fuente vive dentro de `microservicios/microservicio_gestion` y ahora sólo expone `/api/v1/especialidades` y `/api/v1/especialidades/<id>` además del healthcheck.
- Dependencias vía `uv` con `pyproject.toml` (no se usa `requirements.txt`).
- Ejecución local: `cd microservicios/microservicio_gestion`, copiar `.env.example` a `.env`, crear env si querés (`uv venv .venv && .venv\Scripts\activate` en Windows) y `flask run --port 5002`.
- En Docker: `cd docker && cp .env-example .env && docker compose up gestion` (requiere red `mired` ya creada).

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
5. Probá la comunicación entre microservicios usando las URLs internas (`http://gestion:5000`, `http://alumno:8000`, `http://documentacion:5000`) o los puertos publicados hacia tu host.
