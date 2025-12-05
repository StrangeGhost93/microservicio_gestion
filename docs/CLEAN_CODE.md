# Guía de Código Limpio

Esta guía resume los criterios que el proyecto sigue para garantizar un código fácil de leer, extender y probar. Tómalos como checklist antes de crear funcionalidades nuevas.

## 1. Nombrado Intencional
- Usa nombres descriptivos en español consistente (`ProgramaService`, `cohort_resource`).
- Prefiere verbos para acciones (`crear_programa`, `listar_programas`).
- Evita abreviaturas salvo términos de dominio ampliamente usados (e.g. `DTO`, `URI`).

## 2. Funciones Pequeñas y con Propósito
- Cada endpoint delega la lógica a un servicio (`ProgramaService`) y éste a un repositorio, evitando funciones monolíticas.
- Si una función supera ~20 líneas o mezcla preocupaciones (validaciones + persistencia + formateo), divídela.

## 3. Tipado y Validaciones
- Todas las rutas usan `Marshmallow` + `validate_with` para asegurar payloads correctos.
- Añadimos anotaciones de tipo (`Mapping`, `Sequence`) para dejar claro qué espera cada capa.
- Si un parámetro puede ser `None`, indicarlo explícitamente y documentar el comportamiento.

## 4. Manejo de Errores
- Devuelve mensajes explícitos y códigos HTTP consistentes (`404` si no existe, `201` al crear).
- Nunca asumas que un repositorio devuelve datos: valida el `None` antes de operar.
- Registra errores inesperados a nivel `app.logger` y no expongas trazas internas.

## 5. Separación por Capas
- **Resources**: solo parsean request/response.
- **Services**: encapsulan reglas de negocio (no importan `flask.request`).
- **Repositories**: única capa con acceso a `db.session`.
- **Schemas/Validators**: centralizan validaciones y serialización.

## 6. Formato y Documentación
- Cada módulo nuevo debe incluir docstrings breves explicando su objetivo.
- Usa comentarios solo cuando el código no sea autoexplicativo.
- Ejecuta formateadores (como `ruff`/`black`) antes de commitear para mantener estilo consistente.

## 7. Pruebas
- Añade pruebas unitarias por módulo (`tests/test_programas.py`, etc.) cubriendo caminos felices y errores.
- Usa fixtures para preparar datos y evita dependencias entre tests.

## 8. Configuración y Entorno
- Mantén secretos en `.env` y documenta cada variable en `env-example`.
- No compartas `.venv` ni artefactos de build: el `.gitignore` ya los excluye.

## 9. Revisión Continua
- Antes de mergear, corré `pytest` y ejecuta un `docker compose build` para validar integraciones.
- Usa esta guía para tus PR: si algo no cumple, bloquea el merge hasta corregirlo.
