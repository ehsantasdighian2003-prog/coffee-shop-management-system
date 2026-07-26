def test_api_running(client):

    response = client.get("/")

    assert response.status_code == 200