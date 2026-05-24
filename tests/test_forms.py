import pytest
from app import create_app
from forms import ContactForm


@pytest.fixture
def form_app():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False})
    return app


def _make_form(form_app, data):
    with form_app.test_request_context(method="POST", data=data):
        return ContactForm(meta={"csrf": False})


def test_valid_submission_passes(form_app):
    form = _make_form(form_app, {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hi, I would like to discuss a project with you.",
        "hp_field": "",
    })
    assert form.validate() is True


def test_missing_name_fails(form_app):
    form = _make_form(form_app, {
        "name": "",
        "email": "john@example.com",
        "message": "Hi, this is a long enough message.",
        "hp_field": "",
    })
    assert form.validate() is False
    assert "name" in form.errors


def test_invalid_email_fails(form_app):
    form = _make_form(form_app, {
        "name": "Jane",
        "email": "not-an-email",
        "message": "Hi, this is a long enough message.",
        "hp_field": "",
    })
    assert form.validate() is False
    assert "email" in form.errors


def test_short_message_fails(form_app):
    form = _make_form(form_app, {
        "name": "Jane",
        "email": "jane@example.com",
        "message": "too short",
        "hp_field": "",
    })
    assert form.validate() is False
    assert "message" in form.errors
