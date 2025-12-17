# Issue 7: Performance analysis (WSGI vs servidor de desarrollo)

## Objetivo
Medir y documentar rendimiento del microservicio de gestión usando servidor de desarrollo vs WSGI (Gunicorn/Waitress) con la misma carga.

## Criterios de aceptación
- Script o comandos reproducibles para ambos escenarios (dev y WSGI).
- Métricas capturadas: throughput (req/s), latencia media, p95, p99, latencia máx, errores.
- Evidencia adjunta (salida de las pruebas) y breve comparación.

## Alcance
- Endpoint de prueba: `/api/v1/status`.
- Carga base sugerida: 500–1000 requests con concurrencia 50.
- Escenarios:
  - Servidor de desarrollo (Flask `app.py`).
  - Servidor WSGI (Gunicorn en Linux/WSL o Waitress en Windows).

## Pasos recomendados
1) Preparar entorno
- Activar venv, instalar dependencias (incl. `requests`, `waitress` en Windows).
2) Ejecutar benchmark dev
- `python scripts/bench_local.py --mode dev --requests 500 --concurrency 50`
- Guardar salida.
3) Ejecutar benchmark WSGI
- `python scripts/bench_local.py --mode wsgi --requests 500 --concurrency 50`
- Guardar salida.
4) Comparar
- Reportar métricas clave y observar errores/latencias.

## Riesgos
- El servidor de desarrollo no maneja bien concurrencia; puede arrojar muchos errores.
- Gunicorn no corre nativo en Windows; usar WSL o Waitress.

## Resultado esperado
- Evidencia de que WSGI mejora throughput y estabilidad de latencia frente al servidor dev.
