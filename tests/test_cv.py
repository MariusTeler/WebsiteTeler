def test_cv_download_returns_pdf(client):
    response = client.get("/cv")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert response.content_length > 1000
