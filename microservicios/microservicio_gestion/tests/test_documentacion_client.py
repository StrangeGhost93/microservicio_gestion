import requests
def test_especialidades_list(client):
    response = client.get("/api/v1/especialidades")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert {"id", "especialidad", "facultad", "universidad"}.issubset(data[0].keys())
        "_perform_get",
