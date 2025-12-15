def test_especialidad_detail_found(client):
    response = client.get("/api/v1/especialidades/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_especialidad_detail_not_found(client):
    response = client.get("/api/v1/especialidades/9999")

    assert response.status_code == 404
