from app.integrations.documentacion_client import DocumentacionClient


def test_estado_documentacion_ok(client, monkeypatch):
    monkeypatch.setattr(
        DocumentacionClient,
        "estado_servicio",
        classmethod(lambda cls: ({"service": "documentacion", "status": "ok"}, 200)),
    )

    response = client.get("/api/v1/integraciones/documentacion/status")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_estado_documentacion_error(client, monkeypatch):
    monkeypatch.setattr(
        DocumentacionClient,
        "estado_servicio",
        classmethod(lambda cls: ({"service": "documentacion", "status": "error"}, 502)),
    )

    response = client.get("/api/v1/integraciones/documentacion/status")

    assert response.status_code == 502
    assert response.get_json()["status"] == "error"
