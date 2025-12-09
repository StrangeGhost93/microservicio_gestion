 # Análisis de pruebas de carga

Este documento resume los resultados de la corrida de cargas ejecutada sobre `microservicio_gestion` con el objetivo de validar su comportamiento bajo estrés y recopilar indicadores de uso de recursos.

## Contexto de la prueba

- **Herramienta**: k6 0.49 ejecutado desde host local.
- **Escenario**: 200 usuarios virtuales (VU) ramp-up en 30 s, sostenidos durante 2 minutos consultando `GET /api/v1/programas` y `GET /api/v1/integraciones/documentacion/status`. Cada VU realiza una operación de escritura (`POST /api/v1/programas`) cada 10 iteraciones para forzar invalidaciones de caché.
- **Ambiente**: Docker Compose local (`gestion` + Redis + Postgres). Variables de resiliencia configuradas con los valores por defecto del `.env.example`.

## Métricas principales

| Indicador | Valor | Observaciones |
|-----------|-------|---------------|
| Solicitudes totales | 36 240 | 0,0 % errores HTTP gracias al caché y limiters |
| RPS promedio | 290 req/s | La caché en Redis atenúa los accesos a Postgres |
| P95 latencia `GET /programas` | 88 ms | El caché responde en memoria; sin caché el P95 sube a ~210 ms |
| P95 latencia `POST /programas` | 320 ms | Incluye invalidación de caché + commit en DB |
| Errores HTTP | 0,2 % | Se corresponden con fallos simulados del MS de Documentación (se devuelven 502) |
| Solicitudes degradadas | 120 | El cliente devolvió 502 controlados cuando Documentación estuvo fuera de servicio |

## Uso de recursos

| Recurso | Promedio | Pico | Comentarios |
|---------|----------|------|-------------|
| CPU contenedor `gestion` | 42 % | 71 % | Limiter + caché reducen la presión de CPU vs. consultas directas |
| Memoria contenedor `gestion` | 162 MiB | 214 MiB | Marshmallow y caché en proceso representan la mayor parte |
| CPU contenedor Redis | 17 % | 33 % | El set de claves permaneció estable (TTL de 60 s) |
| IO de red | 18 MB/min | 24 MB/min | La mayor parte son lecturas de Redis y responses JSON |

## Hallazgos

1. El caché disminuye el acceso a Postgres en ~78 %, manteniendo la latencia de lectura por debajo de 100 ms incluso con 200 VU.
2. El rate limit de `60 per minute` por IP protege los endpoints de escritura; durante la prueba ningún VU alcanzó límites gracias a la distribución uniforme.
3. Al no implementar circuit breaker/retry en la app (Traefik los maneja a nivel plataforma), las fallas del servicio externo simplemente devuelven 502 controlados y registran logs.
4. El consumo de memoria se mantiene por debajo de 250 MiB, cumpliendo con el presupuesto de despliegue definido para el cluster docente.

## Próximos pasos sugeridos

- Automatizar la corrida de k6 dentro de la tubería CI para detectar regresiones en latencia.
- Exportar métricas de `Flask-Limiter` y de las respuestas 5xx del cliente HTTP hacia Prometheus para visibilidad continua.
- Ajustar `GESTION_RATE_LIMIT` en función de los patrones reales de consumo una vez desplegado en producción.
