def test_index(client):
    response = client.get("/index/")
    assert response.status_code == 200
