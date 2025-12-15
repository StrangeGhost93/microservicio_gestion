def test_healthcheck(client):
    response = client.get("/api/v1/status")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
