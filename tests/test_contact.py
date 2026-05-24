import pytest
import responses


VALID_PAYLOAD = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "message": "Hi Marius, I'd love to chat about a project.",
    "hp_field": "",
}


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
        "CONTACT_RATE_LIMIT": "100 per hour",  # avoid limiter interference in this test
    })


@pytest.fixture
def client(app):
    return app.test_client()


@responses.activate
def test_valid_submission_returns_success_partial(client):
    responses.add(
        responses.POST,
        "https://api.test.example/v3/mg.example.com/messages",
        json={"id": "<x@mg>", "message": "Queued"},
        status=200,
    )
    r = client.post("/contact", data=VALID_PAYLOAD)
    assert r.status_code == 200
    assert b"Thanks" in r.data or b"thanks" in r.data
    assert len(responses.calls) == 1


def test_honeypot_silently_succeeds_no_mail(client):
    # No mock added — if requests goes out, responses raises.
    r = client.post("/contact", data={**VALID_PAYLOAD, "hp_field": "bot"})
    assert r.status_code == 200
    assert b"Thanks" in r.data or b"thanks" in r.data


def test_invalid_payload_returns_form_with_errors(client):
    r = client.post("/contact", data={**VALID_PAYLOAD, "email": "nope"})
    assert r.status_code == 400
    assert b"valid email" in r.data


@responses.activate
def test_mailgun_failure_returns_error_partial(client):
    responses.add(
        responses.POST,
        "https://api.test.example/v3/mg.example.com/messages",
        json={"message": "Forbidden"},
        status=401,
    )
    r = client.post("/contact", data=VALID_PAYLOAD)
    assert r.status_code == 502
    assert b"try email" in r.data or b"try emailing" in r.data
