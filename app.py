from datetime import datetime, timezone

from flask import Flask, render_template, request, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from forms import ContactForm
from mail import send_contact_email


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

    @app.errorhandler(429)
    def too_many_requests(_e):
        return render_template("partials/_contact_error.html"), 429

    @app.get("/healthz")
    def healthz():
        return "ok", 200, {"Content-Type": "text/plain"}

    @app.get("/")
    def index():
        return render_template("index.html", form=ContactForm())

    @app.post("/contact")
    @limiter.limit(lambda: app.config["CONTACT_RATE_LIMIT"])
    def contact_submit():
        form = ContactForm()
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

    @app.get("/cv")
    def download_cv():
        return send_from_directory(
            app.static_folder + "/files",
            "cv-marius-teler.pdf",
            as_attachment=True,
            download_name="Marius-Teler-CV.pdf",
            mimetype="application/pdf",
        )

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now(timezone.utc).year}

    return app


app = create_app()
