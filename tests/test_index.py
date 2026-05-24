def test_index_returns_200_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]
    body = response.get_data(as_text=True)
    assert "Marius Teler" in body
