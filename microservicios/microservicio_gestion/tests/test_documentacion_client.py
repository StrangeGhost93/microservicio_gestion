import requests
from pybreaker import CircuitBreakerError

from app.integrations.documentacion_client import DocumentacionClient


def test_estado_servicio_ok(app, monkeypatch):
    monkeypatch.setattr(
        DocumentacionClient,
        "_perform_get",
        classmethod(lambda cls, path: {"service": "documentacion", "status": "ok"}),
    )

    payload, status_code = DocumentacionClient.estado_servicio()

    assert status_code == 200
    assert payload["status"] == "ok"


def test_estado_servicio_circuit_breaker(app, monkeypatch):
    def _raise_breaker(cls, path):
        raise CircuitBreakerError("documentacion")

    monkeypatch.setattr(DocumentacionClient, "_perform_get", classmethod(_raise_breaker))

    payload, status_code = DocumentacionClient.estado_servicio()

    assert status_code == 503
    assert payload["status"] == "degraded"


def test_estado_servicio_http_error(app, monkeypatch):
    def _raise_request(cls, path):
        raise requests.RequestException("boom")

    monkeypatch.setattr(DocumentacionClient, "_perform_get", classmethod(_raise_request))

    payload, status_code = DocumentacionClient.estado_servicio()

    assert status_code == 502
    assert payload["status"] == "error"
