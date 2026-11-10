import os
from datetime import datetime, timezone
from functools import lru_cache

from flask import Flask, Response, g, render_template, request, send_from_directory, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from content import LANGS, DEFAULT_LANG, PROJECTS_META, STOPS_META, TOOLS, get_content
from cv_content import get_cv
from forms import contact_form_for
from mail import send_contact_email

SITE_URL = "https://teler.net"
CV_FILES = {
    "en": ("cv-marius-teler.pdf", "Marius-Teler-CV.pdf"),
    "ro": ("cv-marius-teler-ro.pdf", "Marius-Teler-CV-RO.pdf"),
}


def create_app(test_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_overrides:
        app.config.update(test_overrides)

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[],
        storage_uri=app.config.get("RATELIMIT_STORAGE_URI", "memory://"),
    )

    # ------------------------------------------------------------------ helpers
    @lru_cache(maxsize=64)
    def _static_version(filename: str) -> str:
        try:
            return str(int(os.path.getmtime(os.path.join(app.static_folder, filename))))
        except OSError:
            return "0"

    def static_v(filename: str) -> str:
        """url_for('static') with an mtime query string, so long cache lifetimes stay safe."""
        return url_for("static", filename=filename, v=_static_version(filename))

    def current_lang() -> str:
        lang = getattr(g, "lang", None)
        if lang in LANGS:
            return lang
        # The contact form posts its language; error pages fall back to the URL prefix.
        posted = request.form.get("lang") if request.method == "POST" else None
        if posted in LANGS:
            return posted
        return "ro" if request.path == "/ro" or request.path.startswith("/ro/") else DEFAULT_LANG

    def home_url(lang: str) -> str:
        return url_for("index_ro") if lang == "ro" else url_for("index")

    def cv_url(lang: str) -> str:
        return url_for("download_cv_ro") if lang == "ro" else url_for("download_cv")

    @app.context_processor
    def inject_globals():
        lang = current_lang()
        other = "en" if lang == "ro" else "ro"
        return {
            "current_year": datetime.now(timezone.utc).year,
            "static_v": static_v,
            "lang": lang,
            "t": get_content(lang),
            "home": home_url(lang),
            "alt_lang": other,
            "alt_home": home_url(other),
            "cv_href": cv_url(lang),
            "site_url": SITE_URL,
            "stops_meta": STOPS_META,
            "projects_meta": PROJECTS_META,
            "tools": TOOLS,
        }

    @app.after_request
    def security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        if request.path.startswith("/static/") and request.args.get("v"):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response

    # ------------------------------------------------------------------ errors
    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404

    @app.errorhandler(429)
    def too_many_requests(_e):
        return render_template("partials/_contact_error.html"), 429

    # ------------------------------------------------------------------ pages
    @app.get("/healthz")
    def healthz():
        return "ok", 200, {"Content-Type": "text/plain"}

    def render_home(lang: str):
        g.lang = lang
        return render_template("index.html", form=contact_form_for(lang))

    @app.get("/")
    def index():
        return render_home("en")

    @app.get("/ro/")
    def index_ro():
        return render_home("ro")

    @app.post("/contact")
    @limiter.limit(lambda: app.config["CONTACT_RATE_LIMIT"])
    def contact_submit():
        lang = current_lang()
        g.lang = lang
        form = contact_form_for(lang)
        # Honeypot: pretend success without sending.
        if form.is_honeypot_filled:
            app.logger.info("Contact honeypot triggered")
            return render_template("partials/_contact_success.html"), 200
        if not form.validate_on_submit():
            return render_template("partials/_contact_form.html", form=form), 400
        ok, _ = send_contact_email(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data,
        )
        if not ok:
            return render_template("partials/_contact_error.html"), 502
        return render_template("partials/_contact_success.html"), 200

    def send_cv(lang: str):
        filename, download_name = CV_FILES[lang]
        return send_from_directory(
            app.static_folder + "/files",
            filename,
            as_attachment=True,
            download_name=download_name,
            mimetype="application/pdf",
        )

    @app.get("/cv")
    def download_cv():
        return send_cv("en")

    @app.get("/ro/cv")
    def download_cv_ro():
        return send_cv("ro")

    @app.get("/cv/preview")
    def cv_preview():
        """HTML source of the PDF CV, used by scripts/make_cv.py. Not linked, not indexed."""
        lang = request.args.get("lang", DEFAULT_LANG)
        g.lang = lang if lang in LANGS else DEFAULT_LANG
        response = Response(render_template("cv.html", cv=get_cv(g.lang)))
        response.headers["X-Robots-Tag"] = "noindex"
        return response

    # ------------------------------------------------------------------ SEO
    @app.get("/robots.txt")
    def robots_txt():
        body = f"User-agent: *\nAllow: /\nDisallow: /cv/preview\nSitemap: {SITE_URL}/sitemap.xml\n"
        return Response(body, mimetype="text/plain")

    @app.get("/sitemap.xml")
    def sitemap_xml():
        alternates = (
            f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}/"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="ro" href="{SITE_URL}/ro/"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/"/>\n'
        )
        body = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            f"  <url>\n    <loc>{SITE_URL}/</loc>\n{alternates}  </url>\n"
            f"  <url>\n    <loc>{SITE_URL}/ro/</loc>\n{alternates}  </url>\n"
            "</urlset>\n"
        )
        return Response(body, mimetype="application/xml")

    return app


app = create_app()
