import os


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-only-secret-do-not-use-in-prod")
    MAILGUN_BASE_URL = os.environ.get("MAILGUN_BASE_URL", "https://api.eu.mailgun.net/v3")
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", "")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", "")
    MAILGUN_FROM = os.environ.get("MAILGUN_FROM", "Website <noreply@example.com>")
    CONTACT_TO_EMAIL = os.environ.get("CONTACT_TO_EMAIL", "")
    CONTACT_RATE_LIMIT = os.environ.get("CONTACT_RATE_LIMIT", "5 per hour")
