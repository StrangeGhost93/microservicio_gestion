"""Cliente HTTP resiliente responsable de hablar con microservicio_documentacion."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import requests
from flask import current_app
from pybreaker import CircuitBreaker, CircuitBreakerError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

_session = requests.Session()


def _build_breaker() -> CircuitBreaker:
    """Crear (o recrear) el circuit breaker con la config actual."""
    return CircuitBreaker(
        fail_max=current_app.config.get("CIRCUIT_MAX_FAILURES", 3),
        reset_timeout=current_app.config.get("CIRCUIT_RESET_TIMEOUT", 30),
    )


class DocumentacionClient:
    """Encapsula llamadas HTTP con retry exponencial + circuit breaker."""

    _breaker: CircuitBreaker | None = None

    @classmethod
    def _breaker_instance(cls) -> CircuitBreaker:
        if cls._breaker is None:
            cls._breaker = _build_breaker()
        return cls._breaker

    @classmethod
    def _base_url(cls) -> str:
        return current_app.config.get("DOCUMENTACION_BASE_URL", "http://localhost:5001")

    @classmethod
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=3),
        retry=retry_if_exception_type(requests.RequestException),
        reraise=True,
    )
    def _perform_get(cls, path: str) -> dict[str, Any]:
        url = urljoin(cls._base_url(), path)
        response = cls._breaker_instance().call(_session.get, url, timeout=3)
        response.raise_for_status()
        return response.json()

    @classmethod
    def estado_servicio(cls) -> tuple[dict[str, Any], int]:
        """Consultar el endpoint de status del microservicio de documentación."""
        try:
            payload = cls._perform_get("/api/v1/status")
            return payload, 200
        except CircuitBreakerError as err:
            current_app.logger.warning("Circuit breaker activo contra documentación: %s", err)
            return {"service": "documentacion", "status": "degraded"}, 503
        except requests.RequestException as err:
            current_app.logger.error("Error consultando documentacion: %s", err)
            return {"service": "documentacion", "status": "error"}, 502
