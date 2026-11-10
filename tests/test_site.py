import re


def test_robots_txt_points_to_sitemap(client):
    r = client.get("/robots.txt")
    assert r.status_code == 200
    assert r.mimetype == "text/plain"
    assert "Sitemap: https://teler.net/sitemap.xml" in r.get_data(as_text=True)


def test_sitemap_lists_homepage(client):
    r = client.get("/sitemap.xml")
    assert r.status_code == 200
    assert r.mimetype == "application/xml"
    assert "<loc>https://teler.net/</loc>" in r.get_data(as_text=True)


def test_unknown_page_returns_branded_404(client):
    r = client.get("/no-such-page")
    assert r.status_code == 404
    body = r.get_data(as_text=True)
    assert "on the route" in body
    assert 'content="noindex"' in body


def test_security_headers_present(client):
    r = client.get("/")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert r.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"


def test_static_assets_are_versioned_and_long_cached(client):
    body = client.get("/").get_data(as_text=True)
    m = re.search(r'href="(/static/css/styles\.css\?v=\d+)"', body)
    assert m, "stylesheet URL should carry a version query string"
    r = client.get(m.group(1))
    assert r.status_code == 200
    assert "immutable" in r.headers["Cache-Control"]


def test_htmx_is_self_hosted_and_swaps_error_responses(client):
    body = client.get("/").get_data(as_text=True)
    assert "unpkg.com" not in body
    assert "/static/js/vendor/htmx-2.0.3.min.js" in body
    # Without this, HTMX 2 silently drops the 400/429/502 partials from /contact.
    assert 'name="htmx-config"' in body and "[2345].." in body


def test_homepage_has_all_sections(client):
    body = client.get("/").get_data(as_text=True)
    for anchor in ("about", "journey", "projects", "expertise", "contact"):
        assert f'id="{anchor}"' in body
