import pytest
import responses


@pytest.fixture
def app():
    from app import create_app
    return create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "MAILGUN_BASE_URL": "https://api.test.example/v3",
        "MAILGUN_DOMAIN": "mg.example.com",
        "MAILGUN_API_KEY": "key-test",
        "MAILGUN_FROM": "Website <noreply@mg.example.com>",
        "CONTACT_TO_EMAIL": "owner@example.com",
        "CONTACT_RATE_LIMIT": "2 per minute",  # tight for testing
        "RATELIMIT_STORAGE_URI": "memory://",
    })


@pytest.fixture
def client(app):
    return app.test_client()


VALID = {"name": "Jane", "email": "j@example.com",
         "message": "A reasonably long message body.", "hp_field": ""}


@responses.activate
def test_third_submission_is_rate_limited(client):
    responses.add(responses.POST,
                  "https://api.test.example/v3/mg.example.com/messages",
                  json={"id": "<x>"}, status=200)

    assert client.post("/contact", data=VALID).status_code == 200
    assert client.post("/contact", data=VALID).status_code == 200
    r = client.post("/contact", data=VALID)
    assert r.status_code == 429
