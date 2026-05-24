from urllib.parse import unquote_plus

import pytest
import responses

from mail import send_contact_email


@pytest.fixture
def mail_app():
    from app import create_app
    return create_app({
        "TESTING": True,
        "MAILGUN_BASE_URL": "https://api.test.example/v3",
        "MAILGUN_DOMAIN": "mg.example.com",
        "MAILGUN_API_KEY": "key-test",
        "MAILGUN_FROM": "Website <noreply@mg.example.com>",
        "CONTACT_TO_EMAIL": "owner@example.com",
    })


@responses.activate
def test_send_contact_email_calls_mailgun(mail_app):
    responses.add(
        responses.POST,
        "https://api.test.example/v3/mg.example.com/messages",
        json={"id": "<abc@mailgun>", "message": "Queued"},
        status=200,
    )
    with mail_app.app_context():
        ok, err = send_contact_email(name="Jane", email="jane@example.com",
                                     message="Hello there")
    assert ok is True
    assert err is None
    assert len(responses.calls) == 1
    body = responses.calls[0].request.body
    if isinstance(body, bytes):
        body = body.decode()
    body = unquote_plus(body)
    assert "Jane" in body
    assert "jane@example.com" in body


@responses.activate
def test_send_contact_email_returns_false_on_error(mail_app):
    responses.add(
        responses.POST,
        "https://api.test.example/v3/mg.example.com/messages",
        json={"message": "Forbidden"},
        status=401,
    )
    with mail_app.app_context():
        ok, err = send_contact_email(name="Jane", email="jane@example.com",
                                     message="Hello there")
    assert ok is False
    assert err is not None
