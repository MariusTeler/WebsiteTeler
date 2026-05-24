from flask import current_app
import requests


def send_contact_email(name: str, email: str, message: str) -> tuple[bool, str | None]:
    cfg = current_app.config
    if not cfg.get("MAILGUN_API_KEY") or not cfg.get("MAILGUN_DOMAIN") or not cfg.get("CONTACT_TO_EMAIL"):
        current_app.logger.error("Mailgun not configured (missing MAILGUN_API_KEY/DOMAIN or CONTACT_TO_EMAIL)")
        return False, "mail_not_configured"

    safe_name = name.replace("\r", " ").replace("\n", " ")[:80]
    url = f"{cfg['MAILGUN_BASE_URL'].rstrip('/')}/{cfg['MAILGUN_DOMAIN']}/messages"
    data = {
        "from": cfg["MAILGUN_FROM"],
        "to": cfg["CONTACT_TO_EMAIL"],
        "subject": f"teler.net contact — {safe_name}",
        "text": (
            f"From: {name} <{email}>\n\n"
            f"{message}\n"
        ),
        "h:Reply-To": email,
    }
    try:
        resp = requests.post(
            url,
            auth=("api", cfg["MAILGUN_API_KEY"]),
            data=data,
            timeout=(3.05, 5),
        )
        resp.raise_for_status()
    except requests.RequestException:
        current_app.logger.exception("Mailgun send failed")
        return False, "upstream_error"
    return True, None
