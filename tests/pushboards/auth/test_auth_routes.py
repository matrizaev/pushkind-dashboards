def test_index(client):
    response = client.get("/auth/")
    assert response.status_code == 200
