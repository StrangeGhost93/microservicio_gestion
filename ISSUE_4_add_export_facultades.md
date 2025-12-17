Título: Issue #4 — Exportar lista de facultades (CSV)

Descripción:
Agregar una nueva funcionalidad al microservicio de gestión para permitir exportar la lista de facultades en formato CSV mediante un endpoint REST.

Objetivo:
- Añadir un endpoint `GET /facultades/export?format=csv` que devuelva un CSV con las facultades existentes.
- Seguir el patrón MVC: controlador/route, servicio, repositorio.
- Aplicar TDD: añadir tests que verifiquen el CSV generado y el comportamiento cuando no hay facultades.
- Respetar KISS/DRY/SOLID: lógica de transformación (object-to-csv) en una función reutilizable en `services` o `utils`; inyección de dependencias para facilitar tests.

Criterios de aceptación:
- Llamada a `GET /facultades/export?format=csv` devuelve `200 OK` y `Content-Type: text/csv` con el CSV.
- CSV contiene cabecera y una línea por facultad con columnas: `id,nombre,abreviatura,ciudad`.
- Test unitarios cubren el servicio generador de CSV y el endpoint (mock del repositorio).

Tareas:
1. Añadir tests (pytest):
   - Test unitario para la función `facultades_to_csv(facultades)`.
   - Test de integración del endpoint con repositorio mock (o base de datos de pruebas).
2. Implementar `facultades_to_csv` en `app/services` o `app/utils/csv.py`.
3. Añadir método en `FacultadRepository` si hace falta para listar con campos específicos.
4. Añadir route/controller `routes/facultades.py` (o extender existente) con la nueva ruta.
5. Ejecutar tests y documentar la API en README o en `docs/`.

Archivos sugeridos a modificar/crear:
- `test/test_export_facultades.py` (nuevo)
- `app/services/csv_utils.py` (nuevo) o `app/services/facultad_service.py` (extender)
- `app/routes/facultades.py` (extender)

Mensaje de commit sugerido:
`#4: Add export CSV endpoint for facultades (tests + implementation)`

Notas:
- Esta tarea es pequeña y proporciona práctica con TDD y separación de responsabilidades.
- Si preferís otro formato (XLSX), agregar parametro `format=xlsx` en una segunda iteración.
