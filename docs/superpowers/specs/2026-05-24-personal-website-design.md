# Personal Website — Marius Teler

**Status:** Draft for review
**Date:** 2026-05-24
**Owner:** Marius Teler Adrian
**Repository:** https://github.com/MariusTeler/WebsiteTeler

---

## 1. Purpose & Audience

A single-page personal website that positions Marius as an experienced **Executive Director with deep IT and operations expertise in the courier industry**. The site doubles as an online business card and a credibility builder for:

- Potential business clients and partners
- Future board / executive opportunities
- Vendor / consulting introductions

Tone: executive, polished, confident. Not a developer-portfolio. Not a generic CV.

## 2. Tech Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Backend | **Flask** (Python) | Matches DSC-Utils stack; tiny app surface; user already fluent |
| Templating | **Jinja2** | Flask-native; partial templates for HTMX swaps |
| Frontend interactivity | **HTMX** (CDN) | User explicitly requested; minimal JS, perfect for contact form swap |
| Custom JS | Vanilla, ~30 lines | Count-up on stats only |
| Styling | **Vanilla CSS** (custom design system, no Bootstrap) | The Executive direction needs refined typography and bespoke layout; Bootstrap defaults would fight the design |
| Forms | **Flask-WTF** + CSRF | Consistent with DSC-Utils security pattern |
| Email | **Mailgun** (consistent with DSC-Utils' `mailgun_tracking` module) | Already familiar; no Gmail SMTP brittleness |
| Hosting | **Railway** (default) | Same provider as DSC-Utils-production; one click deploy from GitHub |
| Python version | 3.11+ | Modern, Railway-supported |
| No database | — | One-page site; contact submissions go straight to email |
| No build step | — | No npm/webpack; CSS served directly |

## 3. Page Structure

Single page (`/`), composed of sections, anchor-linked from the nav:

1. **Nav** (sticky, blur backdrop) — logo, anchors, "Get in touch" CTA
2. **Hero** — eyebrow, headline, lead, two CTAs, animated portrait + floating chips, ambient SVG route animation
3. **Stats bar** — 4 KPIs with count-up on scroll
4. **About** — "Self-taught. Optimizing businesses since 2008." + narrative + "At a glance" card
5. **Journey** — career as a curved courier route with travelling parcel, 7 hub stops
6. **Skills** — 3 cards: Leadership / Technical / Courier Domain
7. **Contact** — contact details + HTMX-powered form
8. **Footer** — copyright + tech credit

Final source of truth for visuals: `.superpowers/brainstorm/3572-1779647170/content/full-mockup-v3.html`. The implementation must match the structure, palette, typography and animations of that mockup.

## 4. Visual Design System

### Palette

```
--ink:        #0b1d36   (navy, primary background)
--ink-2:      #142a4a   (lighter navy, secondary)
--ink-3:      #1d3a66   (accents)
--gold:       #c9a14a   (primary accent)
--gold-bright:#e8c987   (highlights)
--cream:      #f7f3ec   (light section background)
--body:       #2d3748   (body text on light)
--muted:      #6b7280   (muted text)
```

### Typography

- **Headings:** Georgia (system serif), 600 weight; italic gold for emphasis spans
- **Body:** System sans (`-apple-system, BlinkMacSystemFont, sans-serif`)
- **Labels / eyebrows:** uppercase, 11px, 4px letter-spacing, gold

### Components

Defined in `static/css/styles.css`. Components mirror the mockup classes (`.nav`, `.hero`, `.stats`, `.stat`, `.sec`, `.glance-card`, `.journey`, `.route-svg`, `.stop`, `.skill-card`, `.contact`, `.form`).

## 5. Animations

All animations are CSS-driven except the count-up:

| Element | Mechanism | Trigger |
|---------|-----------|---------|
| Hero SVG parcels | `offset-path` + `@keyframes travel` | Continuous |
| Hub ring pulses | `@keyframes pulse-ring` | Continuous, staggered delays |
| Portrait dashed rings | `@keyframes rotate` (30s + 50s reverse) | Continuous |
| Floating chips | `@keyframes float-y` (4–5s ease-in-out) | Continuous |
| Journey route draw | `stroke-dasharray` + `stroke-dashoffset` animation | On page load |
| Journey parcel | `offset-path` + `travel` animation, alternating | Continuous |
| Stop markers pop-in | `@keyframes pop-in`, staggered | On page load (delays 0.5s–3.5s) |
| Last stop live pulse | `@keyframes pulse-marker` | Continuous |
| Stats count-up | `IntersectionObserver` + `requestAnimationFrame` cubic ease | On scroll into view, once |
| Contact "live" dot | `@keyframes live-pulse` | Continuous |
| Skill cards hover | CSS `transform: translateY(-6px)` + box-shadow | On hover |

**Accessibility:** Wrap continuous animations in `@media (prefers-reduced-motion: reduce)` to disable them for users who request it.

## 6. Content (English, final copy)

### Hero
- **Eyebrow:** `Executive Director · Courier IT & Operations`
- **H1:** `Turning courier operations into clean, measurable systems.` (last 5 words in italic gold)
- **Lead:** `Two decades in the courier industry — from the call-center floor to the executive chair. I direct the business, build the software, write the reports, and lead the teams that keep parcels moving and customers happy.`
- **CTAs:** `Work with me →` (primary, scrolls to contact); `Download CV` (ghost, downloads PDF)
- **Floating chips:** `18+ yrs`, `Exec Dir`, `Python · HTMX`

### Stats
- `18+` — Years in logistics IT
- `5` — Courier companies
- `7` — Roles climbed
- `2` — Languages (RO · EN C1)

### About
- **Title:** `Self-taught. Optimizing businesses since 2008.`
- **Paragraph:** `I started as a computer operator at Nemo Express in 2006. Over 14 years I worked my way through customer support, POD coordination and project management to the CIO seat. Since 2022 I've brought that operational fluency to Colete Online, Innoship, and now DSC — Dragon Star Curier, where I serve as Executive Director, also leading IT and Development. My day-to-day sits at the intersection of leadership and code: directing the business while shipping the internal tooling (Python, Flask, HTMX, PostgreSQL) that keeps the operation measurable.`
- **At a glance card:**
  - Based in: Chiajna, RO
  - Current: DSC Dragon Star
  - Stack: Python · Flask · HTMX
  - Languages: RO · EN C1

### Journey (timeline, oldest → newest)
1. `2006` — Network Manager — Inttel Connect
2. `2008–19` — Support & Ops — Nemo Express
3. `2019–21` — Project Manager — Nemo Express
4. `2021–22` — CIO — Nemo Express
5. `2022–23` — IT / Ops — Colete Online
6. `2023–24` — IT / Ops — Innoship
7. `2024 — Now` — Executive Director — DSC · IT & Dev Lead *(last stop, pulses)*

**Detail block (under route):** `From computer operator at the desk to the Executive Director chair — same industry, deeper view at every step. Today I direct DSC Dragon Star Curier with IT and Development under my remit, shipping the internal tooling (DSC-Utils — validations, hub routing, courier analytics) on a Flask + HTMX + PostgreSQL stack that keeps the operation measurable.`

### Skills (3 columns)
- **Leadership:** IT & dev team management; Project scope & stakeholders; Customer support operations; Hiring & performance reviews
- **Technical:** Python, Flask, HTMX; PostgreSQL, SQL reporting; Qlik Sense, ChronoScan; Mediatel call-center stack
- **Courier Domain:** End-to-end courier operations; POD & archive workflows; Data migration between platforms; Hub routing & analytics

### Contact
- **H3:** `Let's move things forward together.` (italic gold on "move things"; "live" green pulse dot at the end)
- **Lead:** `Open to consulting on courier IT, software development partnerships, or full-time leadership roles. Reply within 24h, usually faster.`
- **Channels:**
  - Email: `marius.teler@gmail.com` (`mailto:` link)
  - Phone: `+40 700 64 137` (`tel:` link)
  - Location: Chiajna, Bucharest
  - GitHub: `github.com/MariusTeler`
- **Form fields:** Name, Email, Message → submits via HTMX, replaces form with thank-you partial on success.

### Footer
- `© 2026 Teler Marius Adrian`
- `Built with Python · Flask · HTMX`

## 7. HTMX Integration

Only one HTMX swap in V1: the contact form.

```html
<form hx-post="/contact"
      hx-target="#contact-form-wrap"
      hx-swap="outerHTML"
      hx-indicator="#form-spinner">
  {{ csrf_token() }}
  <input type="text" name="hp_field" class="hp" autocomplete="off" tabindex="-1"> <!-- honeypot -->
  <!-- visible fields -->
</form>
```

- **Success** (`200`): server returns `partials/_contact_response.html` rendered with a thank-you message + reset CTA.
- **Validation error** (`400`): server returns the form partial with `errors` filled in (rendered inline under each field).
- **Server error** (`500`): server returns a generic "couldn't send — try email directly" partial.

## 8. Routes (Flask)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Render `index.html` (full page) |
| POST | `/contact` | Process contact form; return HTMX partial |
| GET | `/cv` | Stream the CV PDF as a download |
| GET | `/healthz` | Liveness probe for Railway |

Static assets served from `/static/`. No other routes in V1.

## 9. Security

- **CSRF**: Flask-WTF `CSRFProtect` global, token rendered in the form template
- **Honeypot**: hidden `hp_field` — non-empty submissions silently dropped (HTTP 200, no email sent)
- **Server-side validation**: name 2–80 chars, email RFC-validated, message 10–4000 chars
- **Rate limiting**: in-process limiter, max 5 submissions per IP per hour (Flask-Limiter)
- **Mailgun secrets**: only in env vars (`MAILGUN_API_KEY`, `MAILGUN_DOMAIN`), never in repo
- **Recipient**: `marius.teler@gmail.com`, hardcoded in env (`CONTACT_TO_EMAIL`)
- **No PII storage**: form data is forwarded to email and discarded; no DB

## 10. File Structure

```
WebsiteTeler/
├── app.py                      # Flask factory + routes
├── config.py                   # Env-driven config
├── forms.py                    # WTForms ContactForm
├── mail.py                     # Mailgun send_message wrapper
├── requirements.txt
├── .env.example                # Documented env vars; no secrets
├── .gitignore                  # .env, .venv, __pycache__, .superpowers/
├── Procfile                    # Railway: `web: gunicorn app:app`
├── runtime.txt                 # python-3.11.x
├── README.md                   # Setup + deploy
├── templates/
│   ├── base.html               # <html>, head meta+og, body skeleton, scripts
│   ├── index.html              # Composes all section partials
│   └── partials/
│       ├── _nav.html
│       ├── _hero.html
│       ├── _stats.html
│       ├── _about.html
│       ├── _journey.html
│       ├── _skills.html
│       ├── _contact.html       # The form (id="contact-form-wrap")
│       ├── _contact_success.html
│       └── _footer.html
├── static/
│   ├── css/
│   │   └── styles.css          # Ported from mockup-v3, organized by section
│   ├── js/
│   │   └── main.js             # Count-up only
│   ├── img/
│   │   ├── portrait.jpg        # Extracted from CV PDF; replace this single file to swap
│   │   └── og-image.png        # 1200×630 social preview
│   └── files/
│       └── cv-marius-teler.pdf # Current CV (Marius will refresh later)
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-05-24-personal-website-design.md
```

## 11. SEO & Social

- `<title>` — `Marius Teler — Executive Director · Courier IT & Operations`
- Meta description (~155 chars)
- OG image, OG title, OG description; Twitter card meta
- `lang="en"` on `<html>`
- `<meta name="robots" content="index, follow">`
- Semantic HTML5 landmarks (`<nav>`, `<main>`, `<section>`, `<footer>`)
- JSON-LD `Person` schema (name, jobTitle, email, sameAs)

## 12. Responsive Behavior

- Desktop: as shown in mockup (max-width 1200px content)
- Tablet (~900px): hero grid collapses to single column, portrait moves above text; stats bar wraps 2×2; journey timeline switches to vertical (stops stacked)
- Mobile (~640px): nav collapses to hamburger; toggle implemented in vanilla JS (~10 lines)
- Touch targets: minimum 44×44px

## 13. Performance

- No external JS frameworks (HTMX is ~14KB gzipped)
- Inline critical CSS (above-the-fold) in `base.html`, defer the rest
- `font-display: swap` if web fonts added later (currently using system fonts)
- Portrait: served as WebP with JPG fallback, ~80KB target
- Total page weight goal: <300KB gzipped (excluding portrait + CV PDF)

## 14. Deployment

- **Railway** project linked to `MariusTeler/WebsiteTeler` GitHub repo
- Auto-deploy on push to `main`
- Required env vars: `FLASK_SECRET_KEY`, `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, `CONTACT_TO_EMAIL`, `PORT` (Railway-provided)
- Custom domain: **teler.net** — configured in Railway with CNAME/A records pointing at the Railway proxy. Implementation plan covers DNS instructions.

## 15. Decisions

Resolved from user review (2026-05-24):

1. **Portrait photo** — extract the headshot from `CV - Teler Marius Adrian.pdf` and use as `static/img/portrait.jpg`. Swap path must be a single file replacement (no markup change).
2. **Phone number on contact** — displayed publicly: `+40 700 64 137`, rendered as a `tel:` link.
3. **Custom domain** — `teler.net`. Railway custom-domain setup + DNS instructions are part of deployment.
4. **CV file** — ship the current CV (`CV - Teler Marius Adrian.pdf`) as-is at `static/files/cv-marius-teler.pdf`. Will be refreshed by Marius later.
5. **Contact form messages locale** — English (validation, success, error).

## 16. Out of Scope (V1)

Deliberately not included; can be follow-up work:

- Multi-language toggle (RO/EN)
- Blog / case studies / project portfolio
- Dark/light theme toggle
- Visitor analytics
- A11y audit beyond reduced-motion + semantic HTML
- E2E test suite (light unit tests for the contact route only in V1)
- Admin dashboard for viewing submissions
