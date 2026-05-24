# Personal Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page personal website for Marius Teler (Executive Director, courier IT) using Flask + HTMX, matching the Executive direction mockup in `.superpowers/brainstorm/3572-1779647170/content/full-mockup-v3.html`, deploy to Railway at `teler.net`.

**Architecture:** Tiny Flask app, single GET route renders `index.html` composed of section partials; one POST route handles the contact form via HTMX with Mailgun-sent email; vanilla CSS ported 1:1 from the mockup; vanilla JS only for count-up and mobile nav; no database, no build step.

**Tech Stack:** Python 3.11, Flask, Flask-WTF, Flask-Limiter, HTMX 2.x, vanilla CSS/JS, Mailgun for outbound email, gunicorn + Railway for hosting.

**User policy reminder (from CLAUDE.md):** `git commit` and `git push` require explicit user approval. The `git commit` steps in this plan are the natural endpoint of each task — pause and ask for permission before running them.

---

## Reference paths

- Spec: `docs/superpowers/specs/2026-05-24-personal-website-design.md`
- Visual source of truth: `.superpowers/brainstorm/3572-1779647170/content/full-mockup-v3.html`
- CV PDF: `/Users/telermarius/Library/CloudStorage/Dropbox/My Stuff/CV - Teler Marius Adrian.pdf`
- Working dir: `/Users/telermarius/Library/CloudStorage/Dropbox/GitHub/WebsiteTeler`
- GitHub repo: `https://github.com/MariusTeler/WebsiteTeler`

---

## Task 1: Initialize git repo + connect to GitHub remote

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Initialize git**

```bash
cd /Users/telermarius/Library/CloudStorage/Dropbox/GitHub/WebsiteTeler
git init -b main
git remote add origin https://github.com/MariusTeler/WebsiteTeler.git
```

- [ ] **Step 2: Create .gitignore**

Create `.gitignore` with:

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
.coverage

# Virtual envs
.venv/
venv/

# Local secrets
.env

# OS
.DS_Store

# Brainstorming session (local-only)
.superpowers/

# Editor
.vscode/
.idea/
```

- [ ] **Step 3: Verify clean status**

Run: `git status`
Expected: untracked: `.gitignore`, `docs/`

- [ ] **Step 4: Ask user for permission, then commit**

```bash
git add .gitignore docs/
git commit -m "chore: initial repo setup with spec and plan"
```

---

## Task 2: Python project skeleton

**Files:**
- Create: `requirements.txt`
- Create: `requirements-dev.txt`
- Create: `.env.example`
- Create: `Procfile`
- Create: `runtime.txt`

- [ ] **Step 1: Create `requirements.txt`**

```
Flask==3.0.3
Flask-WTF==1.2.1
Flask-Limiter==3.8.0
requests==2.32.3
python-dotenv==1.0.1
gunicorn==23.0.0
```

- [ ] **Step 2: Create `requirements-dev.txt`**

```
-r requirements.txt
pytest==8.3.3
pytest-flask==1.3.0
responses==0.25.3
```

- [ ] **Step 3: Create `.env.example`**

```
# Flask
FLASK_SECRET_KEY=change-me-to-a-long-random-string
FLASK_ENV=development

# Mailgun (EU region)
MAILGUN_BASE_URL=https://api.eu.mailgun.net/v3
MAILGUN_DOMAIN=mg.teler.net
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_FROM=Website <noreply@mg.teler.net>

# Contact destination
CONTACT_TO_EMAIL=marius.teler@gmail.com

# Rate limit
CONTACT_RATE_LIMIT=5 per hour
```

- [ ] **Step 4: Create `Procfile`**

```
web: gunicorn "app:create_app()" --workers 2 --bind 0.0.0.0:$PORT --access-logfile -
```

- [ ] **Step 5: Create `runtime.txt`**

```
python-3.11.10
```

- [ ] **Step 6: Create virtualenv and install deps**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
```

Verify: `python -c "import flask; print(flask.__version__)"` prints `3.0.3`.

- [ ] **Step 7: Ask user for permission, then commit**

```bash
git add requirements.txt requirements-dev.txt .env.example Procfile runtime.txt
git commit -m "chore: add Python deps and runtime config"
```

---

## Task 3: Directory structure + empty placeholders

**Files:**
- Create: directory tree per spec section 10

- [ ] **Step 1: Create all directories**

```bash
mkdir -p templates/partials static/css static/js static/img static/files tests
```

- [ ] **Step 2: Create placeholder files so the tree is committable**

```bash
touch templates/.gitkeep templates/partials/.gitkeep
touch static/css/.gitkeep static/js/.gitkeep static/img/.gitkeep static/files/.gitkeep
touch tests/__init__.py
```

- [ ] **Step 3: Verify tree**

Run: `find . -type d -not -path '*/\.*' | sort`
Expected: includes `./templates`, `./templates/partials`, `./static/css`, `./static/js`, `./static/img`, `./static/files`, `./tests`.

(No commit yet — files will be replaced by real ones in later tasks.)

---

## Task 4: Flask app factory + `GET /healthz` (TDD)

**Files:**
- Create: `app.py`
- Create: `config.py`
- Create: `tests/conftest.py`
- Create: `tests/test_health.py`

- [ ] **Step 1: Write the failing test**

`tests/test_health.py`:

```python
def test_healthz_returns_ok(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "ok"
```

- [ ] **Step 2: Create `tests/conftest.py`**

```python
import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_health.py -v`
Expected: FAIL (ImportError on `from app import create_app`).

- [ ] **Step 4: Create `config.py`**

```python
import os


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-only-secret-do-not-use-in-prod")
    MAILGUN_BASE_URL = os.environ.get("MAILGUN_BASE_URL", "https://api.eu.mailgun.net/v3")
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", "")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", "")
    MAILGUN_FROM = os.environ.get("MAILGUN_FROM", "Website <noreply@example.com>")
    CONTACT_TO_EMAIL = os.environ.get("CONTACT_TO_EMAIL", "")
    CONTACT_RATE_LIMIT = os.environ.get("CONTACT_RATE_LIMIT", "5 per hour")
```

- [ ] **Step 5: Create `app.py` with factory + healthz**

```python
from flask import Flask

from config import Config


def create_app(test_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_overrides:
        app.config.update(test_overrides)

    @app.get("/healthz")
    def healthz():
        return "ok", 200, {"Content-Type": "text/plain"}

    return app


app = create_app()
```

- [ ] **Step 6: Run tests to verify pass**

Run: `pytest tests/test_health.py -v`
Expected: 1 passed.

- [ ] **Step 7: Ask user for permission, then commit**

```bash
git add app.py config.py tests/
git commit -m "feat: Flask app factory with /healthz"
```

---

## Task 5: `GET /` returns rendered template (TDD)

**Files:**
- Modify: `app.py`
- Create: `templates/base.html` (minimal)
- Create: `templates/index.html` (minimal)
- Create: `tests/test_index.py`

- [ ] **Step 1: Write the failing test**

`tests/test_index.py`:

```python
def test_index_returns_200_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]
    body = response.get_data(as_text=True)
    assert "Marius Teler" in body
```

- [ ] **Step 2: Run to confirm failure**

Run: `pytest tests/test_index.py -v`
Expected: FAIL (404 Not Found — route doesn't exist yet).

- [ ] **Step 3: Create minimal `templates/base.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}Marius Teler{% endblock %}</title>
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
```

- [ ] **Step 4: Create minimal `templates/index.html`**

```html
{% extends "base.html" %}
{% block content %}
<h1>Marius Teler</h1>
{% endblock %}
```

- [ ] **Step 5: Add `/` route in `app.py`**

Add inside `create_app()` after the `/healthz` route:

```python
    from flask import render_template

    @app.get("/")
    def index():
        return render_template("index.html")
```

(Hoist the `render_template` import to the top of the file for cleanliness.)

- [ ] **Step 6: Run tests**

Run: `pytest -v`
Expected: 2 passed (`test_healthz_returns_ok`, `test_index_returns_200_html`).

- [ ] **Step 7: Ask user for permission, then commit**

```bash
git add app.py templates/
git commit -m "feat: GET / renders index template"
```

---

## Task 6: Port full CSS from mockup v3 to `static/css/styles.css`

**Files:**
- Create: `static/css/styles.css`

- [ ] **Step 1: Extract `<style>` block from the mockup**

Open `.superpowers/brainstorm/3572-1779647170/content/full-mockup-v3.html`. Copy everything between the `<style>` opening tag (right after `<title>`) and its closing `</style>` tag into a new file `static/css/styles.css`.

- [ ] **Step 2: Add reduced-motion guard at the end of `styles.css`**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
  }
  .route-fg { stroke-dashoffset: 0 !important; }
}
```

- [ ] **Step 3: Verify file size sanity**

Run: `wc -l static/css/styles.css`
Expected: 200–350 lines.

- [ ] **Step 4: Ask user for permission, then commit**

```bash
git add static/css/styles.css
git commit -m "feat: port executive-direction styles to styles.css"
```

---

## Task 7: Build `templates/base.html` with head meta, OG, JSON-LD, and asset wiring

**Files:**
- Modify: `templates/base.html`

- [ ] **Step 1: Replace `base.html` with full version**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0b1d36">

  <title>{% block title %}Marius Teler — Executive Director · Courier IT & Operations{% endblock %}</title>
  <meta name="description" content="Two decades in the courier industry — from the call-center floor to the executive chair. I direct DSC Dragon Star Curier with IT and Development under my remit.">
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:type" content="profile">
  <meta property="og:url" content="https://teler.net/">
  <meta property="og:title" content="Marius Teler — Executive Director · Courier IT & Operations">
  <meta property="og:description" content="Self-taught. Optimizing courier businesses since 2008.">
  <meta property="og:image" content="https://teler.net/static/img/og-image.png">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Marius Teler — Executive Director">
  <meta name="twitter:description" content="Self-taught. Optimizing courier businesses since 2008.">
  <meta name="twitter:image" content="https://teler.net/static/img/og-image.png">

  <link rel="icon" type="image/svg+xml" href="{{ url_for('static', filename='img/favicon.svg') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">

  <script src="https://unpkg.com/htmx.org@2.0.3" defer></script>

  <!-- JSON-LD Person schema -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Teler Marius Adrian",
    "jobTitle": "Executive Director",
    "worksFor": { "@type": "Organization", "name": "DSC Dragon Star Curier" },
    "email": "mailto:marius.teler@gmail.com",
    "telephone": "+40700641370",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Chiajna",
      "addressRegion": "Bucharest",
      "addressCountry": "RO"
    },
    "sameAs": [
      "https://github.com/MariusTeler",
      "https://www.facebook.com/marius.teler"
    ],
    "url": "https://teler.net"
  }
  </script>
</head>
<body>
  {% include "partials/_nav.html" %}
  <main>
    {% block content %}{% endblock %}
  </main>
  {% include "partials/_footer.html" %}
  <script src="{{ url_for('static', filename='js/main.js') }}" defer></script>
</body>
</html>
```

- [ ] **Step 2: Create placeholder favicon**

`static/img/favicon.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="14" fill="none" stroke="#c9a14a" stroke-width="3"/>
  <path d="M10 22 L16 10 L22 22 L16 18 Z" fill="#c9a14a"/>
</svg>
```

- [ ] **Step 3: Run server manually to confirm no template errors**

```bash
source .venv/bin/activate
FLASK_SECRET_KEY=dev flask --app app run --port 5050
```

In another terminal: `curl -sI http://localhost:5050/` — expect `200 OK` and HTML headers.
The page won't render fully yet because partials don't exist; stop the server (Ctrl+C). We'll fix in next tasks.

- [ ] **Step 4: Don't commit yet** — broken partials. Will commit after Task 16.

---

## Task 8: Build all 8 section partials from mockup-v3

Each partial mirrors a `<section>` block from the mockup. Content text is finalized in spec section 6. Visual structure must match the mockup exactly.

**Sub-task 8.1 — `_nav.html`**

**File:** Create `templates/partials/_nav.html`

```html
<nav class="nav">
  <div class="logo">
    <svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="14" fill="none" stroke="#c9a14a" stroke-width="1.5"/><path d="M10 22 L16 10 L22 22 L16 18 Z" fill="#c9a14a"/></svg>
    TELER · M
  </div>
  <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">☰</button>
  <ul class="nav-menu">
    <li><a href="#about">About</a></li>
    <li><a href="#journey">Journey</a></li>
    <li><a href="#skills">Skills</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
  <a class="cta" href="#contact">Get in touch</a>
</nav>
```

**Sub-task 8.2 — `_hero.html`**

**File:** Create `templates/partials/_hero.html`

```html
<section class="hero" id="hero">
  <div class="hero-route" aria-hidden="true">
    <svg viewBox="0 0 1400 600" preserveAspectRatio="none">
      <path class="route-path" d="M -50,420 C 200,300 350,500 600,360 S 950,220 1200,340 S 1450,420 1500,300"/>
      <path class="route-path" d="M -50,180 C 150,260 380,140 580,220 S 880,340 1100,200 S 1400,160 1500,250" style="stroke:rgba(201,161,74,.18);"/>
      <g>
        <circle class="hub" cx="200" cy="362" r="3.5"/>
        <circle class="hub-ring" cx="200" cy="362" r="4" style="animation: pulse-ring 3s ease-out infinite;"/>
      </g>
      <g>
        <circle class="hub" cx="700" cy="298" r="3.5"/>
        <circle class="hub-ring" cx="700" cy="298" r="4" style="animation: pulse-ring 3s ease-out infinite 1s;"/>
      </g>
      <g>
        <circle class="hub" cx="1080" cy="332" r="3.5"/>
        <circle class="hub-ring" cx="1080" cy="332" r="4" style="animation: pulse-ring 3s ease-out infinite 2s;"/>
      </g>
      <rect class="parcel" width="10" height="10" x="-5" y="-5" rx="2" style="offset-path: path('M -50,420 C 200,300 350,500 600,360 S 950,220 1200,340 S 1450,420 1500,300'); animation: travel 12s linear infinite;"/>
      <rect class="parcel-2" width="8" height="8" x="-4" y="-4" rx="2" style="offset-path: path('M -50,420 C 200,300 350,500 600,360 S 950,220 1200,340 S 1450,420 1500,300'); animation: travel 12s linear infinite -6s;"/>
      <rect class="parcel" width="9" height="9" x="-4.5" y="-4.5" rx="2" style="offset-path: path('M -50,180 C 150,260 380,140 580,220 S 880,340 1100,200 S 1400,160 1500,250'); animation: travel 14s linear infinite -3s;"/>
    </svg>
  </div>

  <div class="hero-grid">
    <div>
      <div class="eyebrow">Executive Director · Courier IT &amp; Operations</div>
      <h1>Turning courier operations into <em>clean, measurable systems.</em></h1>
      <p class="lead">Two decades in the courier industry — from the call-center floor to the executive chair. I direct the business, build the software, write the reports, and lead the teams that keep parcels moving and customers happy.</p>
      <div class="actions">
        <a class="btn-primary" href="#contact">Work with me →</a>
        <a class="btn-ghost" href="{{ url_for('download_cv') }}">Download CV</a>
      </div>
    </div>
    <div class="portrait-wrap">
      <div class="portrait-ring-2"></div>
      <div class="portrait-ring"></div>
      <img class="portrait" src="{{ url_for('static', filename='img/portrait.jpg') }}" alt="Marius Teler portrait">
      <div class="floating-icon fi-1">18+ yrs</div>
      <div class="floating-icon fi-2">Exec Dir</div>
      <div class="floating-icon fi-3">Python · HTMX</div>
    </div>
  </div>
</section>
```

**CSS adjustment:** the mockup used a `<div class="portrait">` with text inside; this template uses `<img>` instead. Update `.portrait` rule in `styles.css` to add: `object-fit: cover; display: block;`. Remove the placeholder text-centering rules from `.portrait` (`display:flex`, `align-items:center`, `justify-content:center`, font/letter spacing, the `::after` content).

**Sub-task 8.3 — `_stats.html`**

**File:** Create `templates/partials/_stats.html`

```html
<section class="stats" aria-label="Career statistics">
  <div class="stat"><strong data-count="18" data-suffix="+">0</strong><span>Years in logistics IT</span></div>
  <div class="stat"><strong data-count="5" data-suffix="">0</strong><span>Courier companies</span></div>
  <div class="stat"><strong data-count="7" data-suffix="">0</strong><span>Roles climbed</span></div>
  <div class="stat"><strong data-count="2" data-suffix="">0</strong><span>Languages (RO · EN C1)</span></div>
</section>
```

**Sub-task 8.4 — `_about.html`**

**File:** Create `templates/partials/_about.html`

```html
<section class="sec about" id="about" style="max-width:1200px;">
  <div class="sec-label">About</div>
  <h2 class="sec-title">Self-taught. Optimizing businesses since 2008.</h2>
  <div class="about-grid">
    <p>I started as a computer operator at Nemo Express in 2006. Over 14 years I worked my way through customer support, POD coordination and project management to the CIO seat. Since 2022 I've brought that operational fluency to Colete Online, Innoship, and now DSC — Dragon Star Curier, where I serve as <b>Executive Director, also leading IT and Development</b>. My day-to-day sits at the intersection of leadership and code: directing the business while shipping the internal tooling (Python, Flask, HTMX, PostgreSQL) that keeps the operation measurable.</p>
    <div class="glance-card">
      <h4>At a glance</h4>
      <ul>
        <li><span class="label-sm">Based in</span><b>Chiajna, RO</b></li>
        <li><span class="label-sm">Current</span><b>DSC Dragon Star</b></li>
        <li><span class="label-sm">Stack</span><b>Python · Flask · HTMX</b></li>
        <li><span class="label-sm">Languages</span><b>RO · EN C1</b></li>
      </ul>
    </div>
  </div>
</section>
```

**Sub-task 8.5 — `_journey.html`**

**File:** Create `templates/partials/_journey.html`

```html
<section class="journey" id="journey">
  <div class="sec-label" style="justify-content:center;display:flex;">The journey</div>
  <h2 class="sec-title" style="text-align:center;">A 20-year route through the courier industry</h2>

  <div class="route-container">
    <svg class="route-svg" viewBox="0 0 1100 180" preserveAspectRatio="none" aria-hidden="true">
      <path class="route-bg" d="M 50,90 C 180,30 260,150 390,90 S 590,30 720,90 S 870,150 1050,90"/>
      <path class="route-fg" d="M 50,90 C 180,30 260,150 390,90 S 590,30 720,90 S 870,150 1050,90"/>
      <g style="offset-path: path('M 50,90 C 180,30 260,150 390,90 S 590,30 720,90 S 870,150 1050,90'); animation: travel 8s ease-in-out infinite alternate;">
        <rect class="route-parcel" x="-9" y="-9" width="18" height="18" rx="3"/>
      </g>
    </svg>

    <div class="stops">
      <div class="stop">
        <div class="stop-marker"></div>
        <div class="stop-date">2006</div>
        <div class="stop-role">Network Manager</div>
        <div class="stop-co">Inttel Connect</div>
      </div>
      <div class="stop">
        <div class="stop-marker"></div>
        <div class="stop-date">2008–19</div>
        <div class="stop-role">Support &amp; Ops</div>
        <div class="stop-co">Nemo Express</div>
      </div>
      <div class="stop">
        <div class="stop-marker"></div>
        <div class="stop-date">2019–21</div>
        <div class="stop-role">Project Manager</div>
        <div class="stop-co">Nemo Express</div>
      </div>
      <div class="stop">
        <div class="stop-marker"></div>
        <div class="stop-date">2021–22</div>
        <div class="stop-role">CIO</div>
        <div class="stop-co">Nemo Express</div>
      </div>
      <div class="stop">
        <div class="stop-marker"></div>
        <div class="stop-date">2022–23</div>
        <div class="stop-role">IT / Ops</div>
        <div class="stop-co">Colete Online</div>
      </div>
      <div class="stop">
        <div class="stop-marker"></div>
        <div class="stop-date">2023–24</div>
        <div class="stop-role">IT / Ops</div>
        <div class="stop-co">Innoship</div>
      </div>
      <div class="stop">
        <div class="stop-marker"></div>
        <div class="stop-date">2024 — Now</div>
        <div class="stop-role">Executive Director</div>
        <div class="stop-co">DSC · IT &amp; Dev Lead</div>
      </div>
    </div>
  </div>

  <div class="journey-detail">
    <p>From <b>computer operator</b> at the desk to the <b>Executive Director</b> chair — same industry, deeper view at every step. Today I direct DSC Dragon Star Curier with <b>IT and Development</b> under my remit, shipping the internal tooling (<b>DSC-Utils</b> — validations, hub routing, courier analytics) on a Flask + HTMX + PostgreSQL stack that keeps the operation measurable.</p>
  </div>
</section>
```

**Sub-task 8.6 — `_skills.html`**

**File:** Create `templates/partials/_skills.html`

```html
<section class="skills" id="skills">
  <div class="skills-inner">
    <div class="sec-label">Expertise</div>
    <h2 class="sec-title">What I bring to the table</h2>
    <div class="skill-cols">
      <div class="skill-card">
        <div class="skill-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="7" r="4"/><path d="M5 21v-2a7 7 0 0 1 14 0v2"/></svg>
        </div>
        <h4>Leadership</h4>
        <ul>
          <li>IT &amp; dev team management</li>
          <li>Project scope &amp; stakeholders</li>
          <li>Customer support operations</li>
          <li>Hiring &amp; performance reviews</li>
        </ul>
      </div>
      <div class="skill-card">
        <div class="skill-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M16 18l6-6-6-6"/><path d="M8 6l-6 6 6 6"/></svg>
        </div>
        <h4>Technical</h4>
        <ul>
          <li>Python, Flask, HTMX</li>
          <li>PostgreSQL, SQL reporting</li>
          <li>Qlik Sense, ChronoScan</li>
          <li>Mediatel call-center stack</li>
        </ul>
      </div>
      <div class="skill-card">
        <div class="skill-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="M3.27 6.96L12 12.01l8.73-5.05M12 22.08V12"/></svg>
        </div>
        <h4>Courier Domain</h4>
        <ul>
          <li>End-to-end courier operations</li>
          <li>POD &amp; archive workflows</li>
          <li>Data migration between platforms</li>
          <li>Hub routing &amp; analytics</li>
        </ul>
      </div>
    </div>
  </div>
</section>
```

**Sub-task 8.7 — `_contact.html`** (form only — wiring in Task 13)

**File:** Create `templates/partials/_contact.html`

```html
<section class="contact" id="contact">
  <div class="contact-inner">
    <div>
      <div class="sec-label">Contact</div>
      <h3>Let's <em>move things</em><br>forward together.<span class="live-dot"></span></h3>
      <p class="lead-c">Open to consulting on courier IT, software development partnerships, or full-time leadership roles. Reply within 24h, usually faster.</p>
      <ul class="contact-list">
        <li><span class="key">Email</span><a href="mailto:marius.teler@gmail.com" style="color:inherit;">marius.teler@gmail.com</a></li>
        <li><span class="key">Phone</span><a href="tel:+40700641370" style="color:inherit;">+40 700 64 137</a></li>
        <li><span class="key">Location</span>Chiajna, Bucharest</li>
        <li><span class="key">GitHub</span><a href="https://github.com/MariusTeler" style="color:inherit;" rel="noopener">github.com/MariusTeler</a></li>
      </ul>
    </div>
    <div id="contact-form-wrap">
      {% include "partials/_contact_form.html" %}
    </div>
  </div>
</section>
```

**Sub-task 8.8 — `_contact_form.html`** (placeholder; final wiring in Task 13)

**File:** Create `templates/partials/_contact_form.html`

```html
<form class="form" hx-post="{{ url_for('contact_submit') }}" hx-target="#contact-form-wrap" hx-swap="outerHTML">
  {{ form.csrf_token if form else '' }}
  <input type="text" name="hp_field" class="hp" autocomplete="off" tabindex="-1" aria-hidden="true" style="position:absolute;left:-9999px;">
  <label for="name">Your name</label>
  <input id="name" name="name" placeholder="John Doe" required minlength="2" maxlength="80">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" placeholder="john@company.com" required>
  <label for="message">Message</label>
  <textarea id="message" name="message" rows="4" placeholder="What can I help you with?" required minlength="10" maxlength="4000"></textarea>
  <button type="submit">Send message →</button>
</form>
```

**Sub-task 8.9 — `_footer.html`**

**File:** Create `templates/partials/_footer.html`

```html
<footer class="foot">
  <span>© {{ current_year }} Teler Marius Adrian</span>
  <span>Built with Python · Flask · HTMX</span>
</footer>
```

**Sub-task 8.10 — Compose all partials in `index.html`**

Replace `templates/index.html` with:

```html
{% extends "base.html" %}
{% block content %}
{% include "partials/_hero.html" %}
{% include "partials/_stats.html" %}
{% include "partials/_about.html" %}
{% include "partials/_journey.html" %}
{% include "partials/_skills.html" %}
{% include "partials/_contact.html" %}
{% endblock %}
```

**Sub-task 8.11 — Inject `current_year` into base context**

Modify `app.py`. Add inside `create_app()` after route definitions:

```python
    from datetime import datetime

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.utcnow().year}
```

(Hoist `from datetime import datetime` to top imports.)

- [ ] **Step 1: Create files per sub-tasks 8.1 through 8.9**
- [ ] **Step 2: Update `index.html` per sub-task 8.10**
- [ ] **Step 3: Update `app.py` per sub-task 8.11**
- [ ] **Step 4: Update `.portrait` CSS rule per sub-task 8.2's note** in `static/css/styles.css`
- [ ] **Step 5: Run the server** — `flask --app app run --port 5050` — and confirm page loads in browser without 500 errors (some routes like `download_cv` and `contact_submit` will URL-build errors; address those in Tasks 11 and 12). Workaround: temporarily comment out the `Download CV` link and the `hx-post` attribute in the form to verify visual render.
- [ ] **Step 6: Don't commit yet** — defer to Task 13 where contact and CV are real.

---

## Task 9: Extract portrait from CV PDF

**Files:**
- Create: `static/img/portrait.jpg`
- Create: `scripts/extract_portrait.py` (one-off)

- [ ] **Step 1: Install one-off extraction dep**

```bash
source .venv/bin/activate
pip install PyMuPDF==1.24.10 Pillow==10.4.0
```

(Not added to `requirements*.txt` — uninstall after.)

- [ ] **Step 2: Write extraction script**

`scripts/extract_portrait.py`:

```python
"""One-off: extract the largest image from the CV PDF and save as portrait.jpg."""
import io
from pathlib import Path

import fitz
from PIL import Image

CV_PATH = "/Users/telermarius/Library/CloudStorage/Dropbox/My Stuff/CV - Teler Marius Adrian.pdf"
OUT_PATH = Path(__file__).resolve().parent.parent / "static" / "img" / "portrait.jpg"

doc = fitz.open(CV_PATH)
biggest = None
biggest_size = 0
for page in doc:
    for info in page.get_images(full=True):
        xref = info[0]
        base = doc.extract_image(xref)
        img = Image.open(io.BytesIO(base["image"]))
        size = img.size[0] * img.size[1]
        if size > biggest_size:
            biggest = img
            biggest_size = size

if biggest is None:
    raise SystemExit("No images found in PDF")

# Convert to RGB (drop alpha if any) and resize to a sensible web size.
biggest = biggest.convert("RGB")
biggest.thumbnail((600, 600))
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
biggest.save(OUT_PATH, "JPEG", quality=85, optimize=True)
print(f"Saved {biggest.size} to {OUT_PATH}")
```

- [ ] **Step 3: Run the script**

```bash
mkdir -p scripts
# (paste the file above)
python scripts/extract_portrait.py
```

Expected output: `Saved (NNN, NNN) to .../static/img/portrait.jpg`.

- [ ] **Step 4: Visually verify the extracted file**

Open `static/img/portrait.jpg` in Preview. If the wrong image was picked (e.g., a logo larger than the headshot), edit the script to skip by aspect ratio (`abs(w/h - 1) < 0.2`) and rerun.

- [ ] **Step 5: Uninstall the one-off deps**

```bash
pip uninstall -y PyMuPDF Pillow
```

- [ ] **Step 6: Ask user for permission, then commit**

```bash
git add scripts/extract_portrait.py static/img/portrait.jpg
git commit -m "feat: extract and add portrait from CV"
```

---

## Task 10: Copy CV PDF + add `GET /cv` route (TDD)

**Files:**
- Create: `static/files/cv-marius-teler.pdf`
- Modify: `app.py`
- Create: `tests/test_cv.py`

- [ ] **Step 1: Copy the CV**

```bash
cp "/Users/telermarius/Library/CloudStorage/Dropbox/My Stuff/CV - Teler Marius Adrian.pdf" static/files/cv-marius-teler.pdf
```

Verify: `ls -lh static/files/cv-marius-teler.pdf` shows ~380KB.

- [ ] **Step 2: Write the failing test**

`tests/test_cv.py`:

```python
def test_cv_download_returns_pdf(client):
    response = client.get("/cv")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert response.content_length > 1000
```

- [ ] **Step 3: Run to confirm failure**

Run: `pytest tests/test_cv.py -v`
Expected: FAIL (404).

- [ ] **Step 4: Add `/cv` route**

In `app.py`, inside `create_app()`:

```python
    from flask import send_from_directory

    @app.get("/cv")
    def download_cv():
        return send_from_directory(
            app.static_folder + "/files",
            "cv-marius-teler.pdf",
            as_attachment=True,
            download_name="Marius-Teler-CV.pdf",
            mimetype="application/pdf",
        )
```

- [ ] **Step 5: Verify pass**

Run: `pytest tests/test_cv.py -v`
Expected: PASS.

- [ ] **Step 6: Ask user for permission, then commit**

```bash
git add app.py tests/test_cv.py static/files/cv-marius-teler.pdf
git commit -m "feat: serve CV PDF at /cv"
```

---

## Task 11: ContactForm with WTForms validation (TDD)

**Files:**
- Create: `forms.py`
- Create: `tests/test_forms.py`

- [ ] **Step 1: Write the failing test**

`tests/test_forms.py`:

```python
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
```

- [ ] **Step 2: Run to confirm failure**

Run: `pytest tests/test_forms.py -v`
Expected: FAIL (cannot import `ContactForm`).

- [ ] **Step 3: Create `forms.py`**

```python
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        "Your name",
        validators=[DataRequired(message="Please enter your name."),
                    Length(min=2, max=80, message="Name must be 2–80 characters.")],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Please enter your email."),
                    Email(message="Please enter a valid email address.")],
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired(message="Please enter a message."),
                    Length(min=10, max=4000, message="Message must be 10–4000 characters.")],
    )
    hp_field = HiddenField()  # honeypot

    @property
    def is_honeypot_filled(self) -> bool:
        return bool(self.hp_field.data and self.hp_field.data.strip())
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_forms.py -v`
Expected: 4 passed.

- [ ] **Step 5: Ask user for permission, then commit**

```bash
git add forms.py tests/test_forms.py
git commit -m "feat: ContactForm with validation"
```

---

## Task 12: Mailgun client wrapper with mocked tests

**Files:**
- Create: `mail.py`
- Create: `tests/test_mail.py`

- [ ] **Step 1: Write the failing test**

`tests/test_mail.py`:

```python
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
    body = responses.calls[0].request.body.decode()
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
```

- [ ] **Step 2: Run to confirm failure**

Run: `pytest tests/test_mail.py -v`
Expected: FAIL (cannot import `send_contact_email`).

- [ ] **Step 3: Create `mail.py`**

```python
from flask import current_app
import requests


def send_contact_email(name: str, email: str, message: str) -> tuple[bool, str | None]:
    cfg = current_app.config
    url = f"{cfg['MAILGUN_BASE_URL'].rstrip('/')}/{cfg['MAILGUN_DOMAIN']}/messages"
    data = {
        "from": cfg["MAILGUN_FROM"],
        "to": cfg["CONTACT_TO_EMAIL"],
        "subject": f"teler.net contact — {name}",
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
            timeout=10,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        return False, str(exc)
    return True, None
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_mail.py -v`
Expected: 2 passed.

- [ ] **Step 5: Ask user for permission, then commit**

```bash
git add mail.py tests/test_mail.py
git commit -m "feat: Mailgun client for contact form"
```

---

## Task 13: `POST /contact` route + HTMX wiring (TDD)

**Files:**
- Modify: `app.py`
- Modify: `templates/partials/_contact.html`
- Modify: `templates/partials/_contact_form.html`
- Create: `templates/partials/_contact_success.html`
- Create: `templates/partials/_contact_error.html`
- Create: `tests/test_contact.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_contact.py`:

```python
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
```

- [ ] **Step 2: Run to confirm failure**

Run: `pytest tests/test_contact.py -v`
Expected: 4 failures.

- [ ] **Step 3: Create success partial**

`templates/partials/_contact_success.html`:

```html
<div id="contact-form-wrap" class="form" style="text-align:center;">
  <h4 style="font-family:Georgia,serif;color:#c9a14a;margin:0 0 10px;font-size:22px;">Thanks — message sent.</h4>
  <p style="color:#cdd5e0;font-size:14px;margin:0;">I'll get back to you within 24 hours. Usually faster.</p>
</div>
```

- [ ] **Step 4: Create error partial**

`templates/partials/_contact_error.html`:

```html
<div id="contact-form-wrap" class="form" style="text-align:center;">
  <h4 style="font-family:Georgia,serif;color:#c9a14a;margin:0 0 10px;font-size:20px;">Something went wrong.</h4>
  <p style="color:#cdd5e0;font-size:14px;margin:0;">Please try emailing me directly at <a href="mailto:marius.teler@gmail.com" style="color:#c9a14a;">marius.teler@gmail.com</a>.</p>
</div>
```

- [ ] **Step 5: Update `_contact_form.html` to render WTForm field errors**

Replace `templates/partials/_contact_form.html` with:

```html
<form id="contact-form-wrap" class="form" hx-post="{{ url_for('contact_submit') }}" hx-target="#contact-form-wrap" hx-swap="outerHTML">
  {{ form.csrf_token }}
  <input type="text" name="hp_field" class="hp" autocomplete="off" tabindex="-1" aria-hidden="true" style="position:absolute;left:-9999px;">

  <label for="name">Your name</label>
  {{ form.name(id="name", placeholder="John Doe") }}
  {% if form.name.errors %}<div class="form-err">{{ form.name.errors[0] }}</div>{% endif %}

  <label for="email">Email</label>
  {{ form.email(id="email", placeholder="john@company.com") }}
  {% if form.email.errors %}<div class="form-err">{{ form.email.errors[0] }}</div>{% endif %}

  <label for="message">Message</label>
  {{ form.message(id="message", rows=4, placeholder="What can I help you with?") }}
  {% if form.message.errors %}<div class="form-err">{{ form.message.errors[0] }}</div>{% endif %}

  <button type="submit">Send message →</button>
</form>
```

Add the error style to `static/css/styles.css`:

```css
.form-err { color: #fca5a5; font-size: 12px; margin: -14px 0 14px; letter-spacing: .5px; }
```

- [ ] **Step 6: Update `_contact.html` to instantiate the form**

Replace `templates/partials/_contact.html` with the same content as before, but ensure the include passes a form. Since `_contact.html` is rendered inside `index.html`, the form needs to be in the template context. We'll inject it via the route in step 7.

- [ ] **Step 7: Update `app.py` — add `/contact` POST handler and pass form to GET `/`**

Add at the top of `app.py`:

```python
from flask import render_template, request
from forms import ContactForm
from mail import send_contact_email
```

Update the `index` route:

```python
    @app.get("/")
    def index():
        return render_template("index.html", form=ContactForm())
```

Add the contact route:

```python
    @app.post("/contact")
    def contact_submit():
        form = ContactForm()
        # Honeypot: pretend success without sending.
        if form.is_honeypot_filled:
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
```

- [ ] **Step 8: Run tests**

Run: `pytest -v`
Expected: all tests pass.

- [ ] **Step 9: Manual smoke test**

```bash
flask --app app run --port 5050
```

Visit `http://localhost:5050/` in browser. Submit the form with valid data. Without a real Mailgun key, expect the error partial; this is normal in dev — production has the env vars set.

- [ ] **Step 10: Ask user for permission, then commit**

```bash
git add app.py forms.py mail.py templates/partials/ tests/test_contact.py static/css/styles.css
git commit -m "feat: contact form with HTMX + Mailgun + honeypot"
```

---

## Task 14: Rate limiting on `/contact` (TDD)

**Files:**
- Modify: `app.py`
- Create: `tests/test_rate_limit.py`

- [ ] **Step 1: Write the failing test**

`tests/test_rate_limit.py`:

```python
import pytest
import responses


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
        "CONTACT_RATE_LIMIT": "2 per minute",  # tight for testing
        "RATELIMIT_STORAGE_URI": "memory://",
    })


@pytest.fixture
def client(app):
    return app.test_client()


VALID = {"name": "Jane", "email": "j@example.com",
         "message": "A reasonably long message body.", "hp_field": ""}


@responses.activate
def test_third_submission_is_rate_limited(client):
    responses.add(responses.POST,
                  "https://api.test.example/v3/mg.example.com/messages",
                  json={"id": "<x>"}, status=200)

    assert client.post("/contact", data=VALID).status_code == 200
    assert client.post("/contact", data=VALID).status_code == 200
    r = client.post("/contact", data=VALID)
    assert r.status_code == 429
```

- [ ] **Step 2: Run to confirm failure**

Run: `pytest tests/test_rate_limit.py -v`
Expected: FAIL — third request returns 200, not 429.

- [ ] **Step 3: Add Flask-Limiter to `app.py`**

At top of `app.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
```

Inside `create_app()`, before defining routes:

```python
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[],
        storage_uri=app.config.get("RATELIMIT_STORAGE_URI", "memory://"),
    )
```

Decorate the `/contact` route:

```python
    @app.post("/contact")
    @limiter.limit(lambda: app.config["CONTACT_RATE_LIMIT"])
    def contact_submit():
        ...
```

- [ ] **Step 4: Add error handler that returns the error partial**

Inside `create_app()`:

```python
    from flask import render_template as _rt

    @app.errorhandler(429)
    def too_many_requests(_e):
        return _rt("partials/_contact_error.html"), 429
```

(For non-HTMX requests this still renders a fragment — fine since the error fragment is self-styled.)

- [ ] **Step 5: Run tests**

Run: `pytest -v`
Expected: all pass including the new rate-limit test.

- [ ] **Step 6: Ask user for permission, then commit**

```bash
git add app.py tests/test_rate_limit.py
git commit -m "feat: rate-limit contact form to 5/hour"
```

---

## Task 15: Vanilla JS — count-up + mobile nav toggle

**Files:**
- Create: `static/js/main.js`
- Modify: `static/css/styles.css` (mobile nav styles)

- [ ] **Step 1: Create `static/js/main.js`**

```javascript
// Count-up on visible stats
const countObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target;
    const target = parseInt(el.dataset.count, 10);
    const dur = 1400;
    const start = performance.now();
    function step(t) {
      const k = Math.min(1, (t - start) / dur);
      const eased = 1 - Math.pow(1 - k, 3);
      el.firstChild.nodeValue = Math.round(target * eased).toString();
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    countObserver.unobserve(el);
  });
}, { threshold: 0.4 });

document.querySelectorAll('.stat strong').forEach(el => countObserver.observe(el));

// Mobile nav toggle
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    const open = navMenu.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  // Close on nav link click
  navMenu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navMenu.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}
```

- [ ] **Step 2: Add mobile nav CSS to `styles.css`**

Append:

```css
.nav-toggle { display: none; background: none; border: none; color: #fff; font-size: 22px; cursor: pointer; }

@media (max-width: 720px) {
  .nav { padding: 14px 24px; }
  .nav-toggle { display: block; }
  .nav-menu { display: none; position: absolute; top: 100%; left: 0; right: 0; background: rgba(11,29,54,.98); flex-direction: column; gap: 0; padding: 20px 24px; }
  .nav-menu.open { display: flex; }
  .nav-menu li { padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,.08); }
  .nav .cta { display: none; }

  .hero { padding: 50px 24px 60px; min-height: auto; }
  .hero-grid { grid-template-columns: 1fr; gap: 32px; }
  .portrait-wrap { order: -1; }
  .portrait { width: 200px; height: 200px; }
  h1 { font-size: 32px; }

  .stats { grid-template-columns: 1fr 1fr; gap: 24px; padding: 32px 24px; }
  .stat strong { font-size: 36px; }

  section.sec, .skills, .contact, .journey { padding: 56px 24px; }
  .about-grid { grid-template-columns: 1fr; gap: 28px; }
  .skill-cols { grid-template-columns: 1fr; }
  .contact-inner { grid-template-columns: 1fr; gap: 36px; }

  .stops { grid-template-columns: 1fr; gap: 24px; margin-top: 24px; }
  .route-svg { display: none; }
  .stop { text-align: left; padding: 16px; background: rgba(255,255,255,.04); border-left: 3px solid var(--gold); border-radius: 2px; align-items: flex-start; }
  .stop-marker { display: none; }
}
```

- [ ] **Step 3: Verify in browser**

Run server, resize browser to ~600px wide, confirm:
- Hamburger appears
- Menu opens on tap
- Sections stack vertically
- Stats become 2×2
- Timeline becomes vertical card list

- [ ] **Step 4: Ask user for permission, then commit**

```bash
git add static/js/main.js static/css/styles.css
git commit -m "feat: count-up animation + mobile responsive nav"
```

---

## Task 16: OG image placeholder + favicon polish

**Files:**
- Create: `static/img/og-image.png`

- [ ] **Step 1: Generate OG image**

Quickest path: open `.superpowers/brainstorm/3572-1779647170/content/full-mockup-v3.html` in a browser, screenshot the hero section at 1200×630 (use macOS `cmd-shift-4` and crop in Preview), save as `static/img/og-image.png`.

Alternative (programmatic): use Pillow to compose a simple navy/gold OG card with name + title. Acceptable for V1 — refine later.

- [ ] **Step 2: Verify**

```bash
file static/img/og-image.png
```

Expected: PNG, dimensions 1200×630.

- [ ] **Step 3: Ask user for permission, then commit**

```bash
git add static/img/og-image.png
git commit -m "feat: add Open Graph preview image"
```

---

## Task 17: README + dev/run docs

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create `README.md`**

```markdown
# teler.net — personal website

Single-page personal website for Marius Teler Adrian — Executive Director, courier IT & operations.

Built with Flask + HTMX + vanilla CSS. Deployed to Railway at <https://teler.net>.

## Local development

Requires Python 3.11+.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Fill in MAILGUN_* values in .env if you want to test the contact form end-to-end.
flask --app app run --port 5050 --debug
```

Open <http://localhost:5050>.

## Tests

```bash
pytest -v
```

## Deploy (Railway)

1. Connect this GitHub repo to a Railway project.
2. Set env vars on the Railway service: `FLASK_SECRET_KEY`, `MAILGUN_BASE_URL`,
   `MAILGUN_DOMAIN`, `MAILGUN_API_KEY`, `MAILGUN_FROM`, `CONTACT_TO_EMAIL`.
3. Push to `main` — Railway auto-deploys.

### Custom domain (teler.net)

1. In Railway: Service → Settings → Networking → Custom Domain → add `teler.net` and `www.teler.net`.
2. Railway shows a CNAME target like `<project>.up.railway.app`.
3. At your DNS provider, set:
   - `teler.net` — ALIAS/ANAME (or A flat) → Railway target
   - `www.teler.net` — CNAME → Railway target
4. Wait for Railway to provision Let's Encrypt SSL (≤5 minutes).

## Replacing the portrait

Drop a new image at `static/img/portrait.jpg` (recommended: 600×600 JPEG, <100KB).
No template changes needed.
```

- [ ] **Step 2: Ask user for permission, then commit**

```bash
git add README.md
git commit -m "docs: README with setup, test, and deploy instructions"
```

---

## Task 18: Production-ready sanity pass

- [ ] **Step 1: Full test suite**

```bash
pytest -v
```

Expected: all tests pass, no warnings about deprecated APIs.

- [ ] **Step 2: Manual browser walkthrough**

Run `flask --app app run --port 5050 --debug`, then:
- Visit `/` — verify hero, stats, about, journey, skills, contact all render with animations
- Resize browser to 600px — verify mobile layout
- Click "Download CV" — verify PDF downloads
- Submit contact form with invalid email — verify inline error appears, no page reload
- Submit contact form with valid data — verify success partial appears (Mailgun will 401 without real key, you'll see the error partial; this is expected locally)
- Visit `/healthz` — verify "ok"
- DevTools → Lighthouse → run Performance + Accessibility audit; aim ≥90 on both

- [ ] **Step 3: Verify `prefers-reduced-motion`**

DevTools → Rendering → emulate `prefers-reduced-motion: reduce`. Reload. Animations should freeze; route should appear fully drawn.

- [ ] **Step 4: Verify SEO meta tags**

View page source. Check:
- `<title>` and meta description present and not empty
- All `og:*` tags resolve to `https://teler.net/...`
- JSON-LD parses (paste into <https://search.google.com/test/rich-results>)

- [ ] **Step 5: Ask user for permission, then commit any fixes from steps 1–4**

```bash
git add -A
git commit -m "chore: production sanity fixes"
```

---

## Task 19: Push to GitHub and link Railway

- [ ] **Step 1: Ask user for permission, then push**

```bash
git push -u origin main
```

- [ ] **Step 2: Confirm GitHub repo shows all files**

Open <https://github.com/MariusTeler/WebsiteTeler> in browser. Verify the file tree matches.

- [ ] **Step 3: Set up Railway project**

User action (Marius does this in Railway UI):
1. New project → Deploy from GitHub repo → select `MariusTeler/WebsiteTeler`.
2. Railway detects `Procfile` and `runtime.txt`, builds automatically.
3. Add env vars on the service:
   - `FLASK_SECRET_KEY` — generate with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `MAILGUN_BASE_URL=https://api.eu.mailgun.net/v3`
   - `MAILGUN_DOMAIN=mg.teler.net` (or your verified Mailgun domain)
   - `MAILGUN_API_KEY=<from Mailgun dashboard>`
   - `MAILGUN_FROM=Website <noreply@mg.teler.net>`
   - `CONTACT_TO_EMAIL=marius.teler@gmail.com`
   - `CONTACT_RATE_LIMIT=5 per hour`
4. Wait for first successful deploy.
5. Open the Railway-provided URL and verify the site loads.

- [ ] **Step 4: Configure custom domain `teler.net`**

See README "Custom domain" section. Verify HTTPS works on `https://teler.net` and `https://www.teler.net`.

- [ ] **Step 5: Set up Mailgun**

User action:
1. In Mailgun, add and verify `mg.teler.net` (or `teler.net`) as a sending domain.
2. Add DNS records (TXT for SPF/DKIM, MX, CNAME for tracking) at the DNS provider.
3. Copy the API key into Railway env.

- [ ] **Step 6: End-to-end test from production**

Open `https://teler.net`, submit the contact form with a test message. Verify it arrives at `marius.teler@gmail.com`.

---

## Self-Review

**Spec coverage:**
- §1 Purpose/audience — informs copy in Task 8 partials. ✓
- §2 Tech stack — Tasks 2 (deps), 4 (Flask), 6 (CSS), 7 (HTMX script). ✓
- §3 Page structure — Task 8 (all partials). ✓
- §4 Visual design system — Task 6 (CSS ported 1:1). ✓
- §5 Animations — Task 6 (CSS), Task 15 (count-up JS), reduced-motion in Task 6 Step 2. ✓
- §6 Content — Task 8 sub-tasks include final copy from spec. ✓
- §7 HTMX integration — Task 13. ✓
- §8 Routes — Task 4 (/healthz), Task 5 (GET /), Task 10 (/cv), Task 13 (POST /contact). ✓
- §9 Security — Task 11 (validation), Task 13 (honeypot + CSRF), Task 14 (rate limit), env-only secrets in Task 2. ✓
- §10 File structure — Task 3 creates dirs; subsequent tasks fill them. ✓
- §11 SEO — Task 7 (meta + OG + JSON-LD). ✓
- §12 Responsive — Task 15 (mobile CSS). ✓
- §13 Performance — system fonts in Task 6, HTMX via defer in Task 7. ✓
- §14 Deployment — Task 2 (Procfile, runtime), Task 17 (README), Task 19 (Railway + DNS). ✓
- §15 Decisions — portrait extraction (Task 9), phone link (Task 8.7), domain (Task 19), CV (Task 10), English messages (Task 13). ✓
- §16 Out of scope — explicitly not addressed. ✓

**Placeholder scan:** No TBDs, no "implement later", no "similar to Task N". Each step has either exact code, exact commands, or explicit user-action instructions for deployment-only tasks (Task 19) where Marius operates the Railway/Mailgun UIs.

**Type/symbol consistency:**
- `create_app()` used consistently in `app.py`, `tests/conftest.py`, `Procfile`.
- `ContactForm` defined in `forms.py`, used in `app.py` and `tests/test_forms.py`.
- `send_contact_email(name, email, message)` defined in `mail.py`, called in `app.py` `contact_submit()` with matching kwargs.
- Template `#contact-form-wrap` id consistent across `_contact.html`, `_contact_form.html`, `_contact_success.html`, `_contact_error.html`.
- Route names match `url_for()` calls: `download_cv` (Tasks 8.2, 10), `contact_submit` (Tasks 8.8, 13), `index` (implicit), `static` (multiple).
- Env var names match across `.env.example` (Task 2), `config.py` (Task 4), `mail.py` (Task 12), and Railway setup (Task 19).
