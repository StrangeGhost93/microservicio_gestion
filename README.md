# PROYECTO-SYSACAD

**Integrantes:** Juan Destéfano, Occhipinti Julián y Santiago Bruno.

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
