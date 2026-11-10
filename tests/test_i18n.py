import pytest
import responses

from content import CONTENT
from cv_content import CV


def _shape(value):
    """Structure of a content tree: keys for dicts, length + item shapes for lists, type for leaves."""
    if isinstance(value, dict):
        return {k: _shape(v) for k, v in value.items()}
    if isinstance(value, list):
        return [len(value)] + [_shape(v) for v in value]
    return type(value).__name__


@pytest.mark.parametrize("tree", [CONTENT, CV], ids=["site", "cv"])
def test_english_and_romanian_have_the_same_structure(tree):
    assert _shape(tree["en"]) == _shape(tree["ro"])


def test_romanian_homepage(client):
    r = client.get("/ro/")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert '<html lang="ro"' in body
    assert "Ce am construit" in body
    assert 'hreflang="en"' in body and 'hreflang="ro"' in body
    assert 'href="/"' in body  # language switch back to English


def test_english_homepage_links_to_romanian(client):
    body = client.get("/").get_data(as_text=True)
    assert '<html lang="en"' in body
    assert 'href="/ro/"' in body
    assert "Things I&#39;ve built" in body


def test_ro_without_slash_redirects(client):
    r = client.get("/ro")
    assert r.status_code in (301, 308)
    assert r.headers["Location"].endswith("/ro/")


def test_romanian_404(client):
    r = client.get("/ro/nu-exista")
    assert r.status_code == 404
    assert "nu e pe traseu" in r.get_data(as_text=True)


def test_romanian_cv_download(client):
    r = client.get("/ro/cv")
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/pdf"
    assert "Marius-Teler-CV-RO.pdf" in r.headers["Content-Disposition"]


@pytest.mark.parametrize("lang,needle", [("en", "Executive Director"), ("ro", "Director Executiv")])
def test_cv_preview_renders_each_language(client, lang, needle):
    r = client.get(f"/cv/preview?lang={lang}")
    assert r.status_code == 200
    assert needle in r.get_data(as_text=True)
    assert r.headers["X-Robots-Tag"] == "noindex"


def test_cv_leaves_out_private_details(client):
    for lang in ("en", "ro"):
        body = client.get(f"/cv/preview?lang={lang}").get_data(as_text=True)
        assert "22/07/1986" not in body
        assert "Sebe Costin" not in body


@pytest.fixture
def mail_app():
    from app import create_app
    return create_app({
        "TESTING": True, "WTF_CSRF_ENABLED": False,
        "MAILGUN_BASE_URL": "https://api.test.example/v3", "MAILGUN_DOMAIN": "mg.example.com",
        "MAILGUN_API_KEY": "key-test", "MAILGUN_FROM": "Website <noreply@mg.example.com>",
        "CONTACT_TO_EMAIL": "owner@example.com", "CONTACT_RATE_LIMIT": "100 per hour",
    })


def test_romanian_form_errors_are_in_romanian(mail_app):
    r = mail_app.test_client().post("/contact", data={"lang": "ro", "name": "M", "email": "x", "message": "", "hp_field": ""})
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert "adresă de email validă" in body
    assert 'name="lang" value="ro"' in body


@responses.activate
def test_romanian_success_message(mail_app):
    responses.add(responses.POST, "https://api.test.example/v3/mg.example.com/messages", json={"id": "<x>"}, status=200)
    r = mail_app.test_client().post("/contact", data={
        "lang": "ro", "name": "Maria", "email": "maria@example.com",
        "message": "Bună ziua, aș vrea să discutăm.", "hp_field": ""})
    assert r.status_code == 200
    assert "Mulțumesc" in r.get_data(as_text=True)


def test_unknown_language_falls_back_to_english(mail_app):
    r = mail_app.test_client().post("/contact", data={"lang": "xx", "name": "M", "email": "x", "message": "", "hp_field": ""})
    assert "valid email" in r.get_data(as_text=True)
