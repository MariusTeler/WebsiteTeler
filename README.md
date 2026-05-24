# teler.net — personal website

Single-page personal website for Marius Teler Adrian — Executive Director, courier IT & operations.

Built with Flask + HTMX + vanilla CSS. Deployed to Railway at <https://teler.net>.

## Local development

Requires Python 3.13+ (Railway uses the version pinned in `runtime.txt`).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Fill in MAILGUN_* values in .env if you want to test the contact form end-to-end.
flask --app app run --port 5050 --debug
```

Open <http://localhost:5050>.

## Tests

```bash
.venv/bin/pytest -v
```

Current count: 14 tests covering health, index, CV download, contact form validation, Mailgun client, contact route (HTMX swap, honeypot, validation errors, upstream failure), and rate limiting.

## Deploy (Railway)

1. Connect this GitHub repo to a Railway project.
2. Set env vars on the Railway service:
   - `FLASK_SECRET_KEY` — generate with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `MAILGUN_BASE_URL` — `https://api.eu.mailgun.net/v3`
   - `MAILGUN_DOMAIN` — e.g. `mg.teler.net`
   - `MAILGUN_API_KEY` — from Mailgun dashboard
   - `MAILGUN_FROM` — e.g. `Website <noreply@mg.teler.net>`
   - `CONTACT_TO_EMAIL` — `marius.teler@gmail.com`
   - `CONTACT_RATE_LIMIT` — `5 per hour`
3. Push to `main` — Railway auto-deploys via `Procfile` + `runtime.txt`.

### Custom domain (teler.net)

1. In Railway: Service → Settings → Networking → Custom Domain → add `teler.net` and `www.teler.net`.
2. Railway shows a CNAME target like `<project>.up.railway.app`.
3. At your DNS provider, set:
   - `teler.net` — ALIAS/ANAME (or flat A) → Railway target
   - `www.teler.net` — CNAME → Railway target
4. Wait for Railway to provision Let's Encrypt SSL (≤5 minutes).

### Mailgun setup

1. In Mailgun, add and verify `mg.teler.net` (or `teler.net`) as a sending domain.
2. Add the DNS records Mailgun prescribes (TXT for SPF/DKIM, MX, CNAME for tracking).
3. Copy the API key into the Railway env (`MAILGUN_API_KEY`).

## Project structure

```
.
├── app.py                   # Flask factory + routes
├── config.py                # Env-driven config class
├── forms.py                 # WTForms ContactForm (with honeypot)
├── mail.py                  # Mailgun client wrapper
├── requirements.txt         # Production deps
├── requirements-dev.txt     # + pytest, responses
├── Procfile                 # gunicorn config for Railway
├── runtime.txt              # Python version pin
├── templates/
│   ├── base.html            # Head, SEO, OG, JSON-LD, body skeleton
│   ├── index.html           # Composes all section partials
│   └── partials/            # _nav, _hero, _stats, _about, _journey,
│                            # _skills, _contact, _contact_form,
│                            # _contact_success, _contact_error, _footer
├── static/
│   ├── css/styles.css       # Single stylesheet (~200 lines)
│   ├── js/main.js           # Count-up + mobile nav toggle
│   ├── img/                 # portrait.jpg, og-image.png, favicon.svg
│   └── files/               # cv-marius-teler.pdf
├── tests/                   # 14 pytest tests
├── scripts/
│   ├── extract_portrait.py  # One-off: pull headshot from CV PDF
│   └── make_og_image.py     # One-off: generate the OG preview PNG
└── docs/superpowers/        # Spec + plan + brainstorm history
```

## Replacing the portrait

Drop a new image at `static/img/portrait.jpg` (recommended: square, 600×600 JPEG, <100KB). No template changes needed — the layout treats the file as a single swap point.

## Regenerating the OG image

```bash
pip install Pillow
python scripts/make_og_image.py
pip uninstall Pillow
```
