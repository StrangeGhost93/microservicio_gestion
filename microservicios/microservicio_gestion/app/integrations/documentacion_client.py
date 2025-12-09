"""Cliente HTTP responsable de hablar con microservicio_documentacion."""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import requests
from flask import current_app

_session = requests.Session()


class DocumentacionClient:
    """Encapsula llamadas HTTP simples hacia microservicio_documentacion."""

    @classmethod
    def _base_url(cls) -> str:
        return current_app.config.get("DOCUMENTACION_BASE_URL", "http://localhost:5001")

    @classmethod
    def _timeout(cls) -> float:
        return float(current_app.config.get("DOCUMENTACION_TIMEOUT", 3))

    @classmethod
    def _perform_get(cls, path: str) -> dict[str, Any]:
        url = urljoin(cls._base_url(), path)
        response = _session.get(url, timeout=cls._timeout())
        response.raise_for_status()
        return response.json()

    @classmethod
    def estado_servicio(cls) -> tuple[dict[str, Any], int]:
        """Consultar el endpoint de status del microservicio de documentación."""
        try:
            payload = cls._perform_get("/api/v1/status")
            return payload, 200
        except requests.RequestException as err:
            current_app.logger.error("Error consultando documentacion: %s", err)
            return {"service": "documentacion", "status": "error"}, 502
