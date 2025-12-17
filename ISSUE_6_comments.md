Título: Issue #6 — Comentarios en código (Patrones y Seguridad)

Descripción breve:
He agregado comentarios en el código señalando los patrones de microservicios usados y recomendaciones de seguridad en los Dockerfile. Este issue agrupa esos comentarios y sirve como base para revisión.

Archivos con comentarios agregados:
- `microservicios/microservicio_gestion/app/routes/facultades.py` — comentario sobre responsabilidad del controller y enlace al servicio.
- `microservicios/microservicio_gestion/app/services/facultad_service.py` — comentario sobre Service Layer y Single Responsibility.
- `microservicios/microservicio_gestion/app/repositories/facultad_repositorio.py` — comentario sobre Repository Pattern y manejo de commits.
- `microservicios/microservicio_gestion/app/resources/__init__.py` — comentario sobre blueprints y modularidad.
- `microservicios/microservicio_gestion/Dockerfile` y `Dockerfile` — bloque de mejores prácticas de seguridad ya añadido.

Pasos sugeridos:
1. Revisar los comentarios y, si están correctos, crear un PR que los documente oficialmente.
2. Opcional: extraer recomendaciones en un documento `SECURITY.md` y aplicar a otros Dockerfiles.

Commit sugerido:
`#6: Add comments summarizing patterns and security notes`

Notas:
- Este archivo es un resumen; los comentarios ya están presentes en los archivos mencionados.
