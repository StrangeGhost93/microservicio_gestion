import pytest

from app.resources.program_resource import _parse_bool, ProgramaService


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),
        ("true", True),
        ("1", True),
        ("SI", True),
        ("false", False),
        ("0", False),
        ("no", False),
    ],
)
def test_parse_bool(value, expected):
    assert _parse_bool(value) is expected


def test_listar_programas_interpreta_vigente(client, monkeypatch):
    recorder = {}

    def _fake_listar(vigente):
        recorder["vigente"] = vigente
        return []

    monkeypatch.setattr(ProgramaService, "listar", staticmethod(_fake_listar))

    response = client.get("/api/v1/programas?vigente=Si")

    assert response.status_code == 200
    assert recorder["vigente"] is True


def test_listar_programas_sin_parametro(client, monkeypatch):
    recorder = {}

    def _fake_listar(vigente):
        recorder["vigente"] = vigente
        return []

    monkeypatch.setattr(ProgramaService, "listar", staticmethod(_fake_listar))

    response = client.get("/api/v1/programas")

    assert response.status_code == 200
    assert recorder["vigente"] is None
