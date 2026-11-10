"""All visible copy for teler.net, in English and Romanian.

Templates read from `t` (one of the dicts below), so a text change happens in one place
and the two languages stay structurally identical. `test_content.py` checks that.
"""

LANGS = ("en", "ro")
DEFAULT_LANG = "en"

STOPS_META = [
    {"year": "2006"}, {"year": "2008"}, {"year": "2019"}, {"year": "2021"},
    {"year": "2022"}, {"year": "2023"}, {"year": "2024"},
]

# Language-neutral project data: slug, status, links, stack, visual.
PROJECTS_META = [
    {"slug": "dsc", "host": "curierdragonstar.ro", "status": "live", "url": "https://www.curierdragonstar.ro/", "image": "img/projects/dsc.jpg",
     "stack": ["PHP", "MariaDB", "CMS", "Bootstrap"], "size": "wide"},
    {"slug": "servicehub", "host": "servicehub / avize", "status": "testing", "url": None, "image": None, "visual": "kanban",
     "stack": ["Flask", "SQLAlchemy", "PostgreSQL", "HTMX", "WeasyPrint"]},
    {"slug": "flota", "host": "flota.dsc / documente", "status": "internal", "url": None, "image": None, "visual": "fleet",
     "stack": ["Flask", "PostgreSQL", "HTMX", "Alpine.js", "Tailwind"]},
    {"slug": "new4you", "host": "new4you.ro", "status": "live", "url": "https://new4you.ro/", "image": "img/projects/new4you.jpg",
     "stack": ["WordPress", "WooCommerce", "PHP", "Docker"]},
    {"slug": "willy", "host": "willycarservice.ro", "status": "live", "url": "https://willycarservice.ro/", "image": "img/projects/willy.jpg",
     "stack": ["Flask", "Jinja", "CSS"]},
]

TOOLS = ["Python", "Flask", "HTMX", "PostgreSQL", "PHP", "WooCommerce", "Mailgun", "e-Factura",
         "Qlik Sense", "Courier Manager", "Mediatel", "Live Agent", "ChronoScan"]

CONTENT = {
    # ======================================================================
    "en": {
        "lang": "en",
        "locale": "en_US",
        "meta": {
            "title": "Marius Teler, Executive Director: courier IT and operations",
            "description": "Twenty years in the courier industry, from the customer desk to the director's chair. "
                           "Marius Teler directs DSC Dragon Star Curier and builds the software that runs it.",
            "og_description": "Self-taught. Optimizing courier businesses since 2008.",
        },
        "nav": {
            "skip": "Skip to content",
            "home_label": "Marius Teler, back to top",
            "sections": "Sections",
            "about": "About", "journey": "Journey", "projects": "Projects",
            "expertise": "Expertise", "contact": "Contact",
            "cta": "Get in touch",
            "menu_open": "Open menu", "menu_close": "Close menu",
            "cv": "Download CV",
            "switch_label": "Citește în română",
        },
        "hero": {
            "intro": "Marius Teler, Executive Director at DSC Dragon Star Curier",
            "title": "Turning courier operations into clean, measurable systems.",
            "title_lines": ["Turning courier", "operations into clean,", "measurable systems"],
            "lead": "Twenty years in the courier industry, from the customer desk to the director's chair. "
                    "I run the business, build the software, and lead the teams that keep parcels moving.",
            "cta": "Work with me",
            "cv": "Download CV",
            "portrait_alt": "Portrait of Marius Teler",
            "tracking_label": "Career, told as a parcel tracking card",
            "tracking_id": "Tracking no. MT2006",
            "tracking_chip": "In transit",
            "steps": [
                ["Picked up", "Inttel Connect, 2006"],
                ["Sorted", "Nemo Express, 2008 to 2022"],
                ["Transferred", "Colete Online, Innoship"],
                ["Out for delivery", "DSC Dragon Star, now"],
            ],
            "ledger_label": "Career in numbers",
            "ledger": [
                ["Years in IT", 20, ""],
                ["Years in the courier industry", 18, "+"],
                ["Roles, desk to director", 7, ""],
                ["Courier companies", 4, ""],
            ],
            "marquee_label": "Tools and domains I work with",
            "marquee_extra": ["SQL reporting", "Hub routing", "POD workflows", "Data migration", "Courier analytics"],
        },
        "about": {
            "kicker": "About",
            "statement": "I learned the courier business from the inside: answering complaints, scanning PODs, "
                         "running support, rolling out new software. Today I direct the company and still write "
                         "the code that measures it.",
            "paragraphs": [
                "I joined Nemo Express in 2008 on the customer complaints desk and stayed fourteen years, moving "
                "through POD coordination, customer support management and project management to the CIO seat. "
                "Along the way I rolled out Live Agent, Courier Manager and the Mediatel contact center, and moved "
                "years of data off the legacy system.",
                "After that I worked on the platform side of delivery at Colete Online and Innoship. Since 2024 "
                "I've been Executive Director of DSC Dragon Star Curier, with IT and Development under my remit. "
                "Most days sit between leadership and code: running the business while shipping the internal tools "
                "that keep the operation measurable.",
            ],
            "facts": [
                ["Based in", "Chiajna, Bucharest"],
                ["Currently", "Executive Director, DSC Dragon Star Curier"],
                ["Builds with", "Python, Flask, HTMX, PostgreSQL"],
                ["Languages", "Romanian, English (C1)"],
            ],
        },
        "journey": {
            "kicker": "Journey",
            "title": "A 20-year route through the courier industry",
            "count": "of {n} stops",
            "stops": [
                {"when": "2006 to 2008", "role": "Network Manager", "co": "Inttel Connect",
                 "text": "Local network management: installs, troubleshooting and client support. "
                         "The first job where fixing things was the job."},
                {"when": "2008 to 2019", "role": "Customer support, POD and operations", "co": "Nemo Express",
                 "text": "Started on the complaints desk, coordinated the POD scanning team and archive, then managed "
                         "customer support: policies, hiring, reporting. Rolled out Live Agent."},
                {"when": "2019 to 2021", "role": "Project Manager", "co": "Nemo Express",
                 "text": "Led the Courier Manager rollout: scope, stakeholders and vendors, customization, and "
                         "migrating years of data off the legacy database."},
                {"when": "2021 to 2022", "role": "Chief Information Officer", "co": "Nemo Express",
                 "text": "Ran the IT and development team, the courier platform and the Mediatel contact center, "
                         "keeping systems aligned with business goals."},
                {"when": "2022 to 2023", "role": "IT and Operations", "co": "Colete Online",
                 "text": "IT and operations for an online courier booking platform, seeing the industry from the "
                         "marketplace side."},
                {"when": "2023 to 2024", "role": "IT and Operations", "co": "Innoship",
                 "text": "IT and operations for a multi-carrier delivery platform, connecting shippers to many "
                         "couriers at once."},
                {"when": "2024 to now", "role": "Executive Director", "co": "DSC Dragon Star Curier",
                 "text": "Directing the business with IT and Development under my remit. I built DSC-Utils, the "
                         "in-house platform for validations, hub routing and courier analytics, and the new company "
                         "website."},
            ],
        },
        "projects": {
            "kicker": "Projects",
            "title": "Things I've built",
            "intro": "Websites and applications I designed and built myself, for DSC and for other businesses.",
            "status": {"live": "Live", "testing": "In testing", "internal": "In-house"},
            "visit": "Visit site",
            "preview_label": "Screenshot of {name}",
            "items": {
                "dsc": {
                    "name": "Dragon Star Curier website",
                    "kind": "Company website, 2026",
                    "text": "The new public website of DSC, rebuilt on the existing PHP CMS: an animated map of the "
                            "network with its 5 hubs and every agency, a homepage panel to track, send or price a "
                            "parcel, online booking with the AWB label sent by email, a fuel index page, a blog and "
                            "an SEO page for each agency. Every block stays editable from the admin.",
                },
                "servicehub": {
                    "name": "ServiceHub",
                    "kind": "Software for car repair shops, 2026",
                    "text": "A multi-tenant management app for car repair shops, with each company's data isolated "
                            "at the ORM level. Quotes and work orders on a Kanban board, appointments, customers and "
                            "vehicles, parts stock, invoicing with submission to RO e-Factura (ANAF), PDF documents, "
                            "email through Mailgun, and ITP, insurance and service reminders.",
                    "visual": {"columns": ["New", "In progress", "Waiting for parts", "Ready"],
                               "cards": ["Brake pads", "Oil service", "Diagnostics", "A/C refill", "Timing belt"]},
                },
                "flota": {
                    "name": "Flota DSC",
                    "kind": "Fleet management, 2025 to 2026",
                    "text": "Fleet management for a courier company: vehicles, drivers and assignments, documents "
                            "with expiry alerts (ITP, insurance, licences), service and maintenance, fuel and "
                            "operating costs, notification rules and Excel or PDF exports. A layered Flask app "
                            "with more than 100 API endpoints.",
                    "visual": {"head": ["Vehicle", "ITP", "Insurance"],
                               "rows": [["Van 01", ["in 12 days", "warn"], ["valid", "ok"]],
                                        ["Van 02", ["valid", "ok"], ["in 4 days", "alert"]],
                                        ["Truck 03", ["valid", "ok"], ["valid", "ok"]]],
                               "note": "2 documents expire this month"},
                },
                "new4you": {
                    "name": "New4you.ro",
                    "kind": "Online store, 2026",
                    "text": "Moved a licensed kids' clothing store from OpenCart 2.3 to WooCommerce with a custom "
                            "block theme. The migration is automated and can be re-run: products and variants, "
                            "customers with their existing passwords, order history, and 301 redirects for every "
                            "old URL. Plus the contract withdrawal flow the law requires.",
                },
                "willy": {
                    "name": "Willy Car Service",
                    "kind": "Business website, 2026",
                    "text": "A presentation website for a car repair shop in Domnești: services, gallery, team, "
                            "hiring announcements, map and contact, with the call button always one tap away on "
                            "mobile.",
                },
            },
            "inhouse_title": "And the tools only DSC sees",
            "inhouse_intro": "Most of my code runs inside the company, on DSC-Utils and around it.",
            "inhouse": [
                ["Statistics dashboard", "Volumes, statuses and KPIs per hub and station, in one place for management."],
                ["Courier analysis", "Delivery performance per courier, so coaching starts from numbers."],
                ["Notification campaigns", "Personalized emails with Word attachments to the whole client base through Mailgun, with an archive and a delivery report."],
                ["Settlement validation", "Matches cash-on-delivery settlements against bank deposits, automatically and by hand."],
                ["Hub routing and zones", "Sends each shipment to the right hub and maps every locality to a delivery zone."],
                ["Lost-client analysis", "Finds the clients who stopped shipping, and since when."],
                ["Unidentified parcels", "A photo registry for parcels without a readable label, until each one finds its owner."],
            ],
        },
        "expertise": {
            "kicker": "Expertise",
            "title": "What I bring to the table",
            "areas": [
                {"title": "Leadership", "line": "Building teams that run well without me in the room.",
                 "points": ["IT and development teams", "Project scope and stakeholders",
                            "Customer support operations", "Hiring and performance reviews"]},
                {"title": "Technology", "line": "Software that turns daily operations into numbers you can act on.",
                 "points": ["Python, Flask, HTMX", "PostgreSQL and SQL reporting", "PHP, WordPress, WooCommerce",
                            "Courier Manager, Mediatel, Live Agent"]},
                {"title": "Courier operations", "line": "Every step a parcel takes, from pickup to proof of delivery.",
                 "points": ["End-to-end courier operations", "POD and archive workflows",
                            "Data migration between platforms", "Hub routing and analytics"]},
            ],
        },
        "contact": {
            "kicker": "Contact",
            "title": "Let's move things forward.",
            "lead": "Open to consulting on courier IT, software partnerships and leadership roles. "
                    "I reply within 24 hours, usually sooner.",
            "keys": {"email": "Email", "phone": "Phone", "location": "Location", "github": "GitHub"},
            "location": "Chiajna, Bucharest",
            "copy_label": "Copy email address", "copied": "Copied", "copy_fallback": "Press Ctrl+C",
            "form_title": "Send a message",
            "name": "Your name", "email": "Email", "message": "How can I help?",
            "submit": "Send message", "sending": "Sending",
            "success_title": "Thanks, your message was delivered.",
            "success_text": "I'll reply within 24 hours, usually sooner.",
            "error_title": "The message didn't go through.",
            "error_text": "Please try emailing me directly at",
        },
        "footer": {"elsewhere": "Elsewhere", "email": "Email", "cv": "CV", "top": "Back to top"},
        "notfound": {
            "title": "Page not found, teler.net",
            "heading": "This address isn't on the route.",
            "text": "The page may have moved, or the link has a typo. The homepage has everything on this site.",
            "cta": "Go to the homepage",
        },
    },
    # ======================================================================
    "ro": {
        "lang": "ro",
        "locale": "ro_RO",
        "meta": {
            "title": "Marius Teler, Director Executiv: IT și operațiuni în curierat",
            "description": "Douăzeci de ani în curierat, de la biroul de relații cu clienții până la scaunul de "
                           "director. Marius Teler conduce DSC Dragon Star Curier și construiește software-ul care o face să meargă.",
            "og_description": "Autodidact. Optimizez companii de curierat din 2008.",
        },
        "nav": {
            "skip": "Sari la conținut",
            "home_label": "Marius Teler, înapoi sus",
            "sections": "Secțiuni",
            "about": "Despre", "journey": "Traseu", "projects": "Proiecte",
            "expertise": "Expertiză", "contact": "Contact",
            "cta": "Hai să vorbim",
            "menu_open": "Deschide meniul", "menu_close": "Închide meniul",
            "cv": "Descarcă CV-ul",
            "switch_label": "Read in English",
        },
        "hero": {
            "intro": "Marius Teler, Director Executiv la DSC Dragon Star Curier",
            "title": "Transform curieratul în sisteme clare și măsurabile.",
            "title_lines": ["Transform curieratul", "în sisteme clare", "și măsurabile"],
            "lead": "Douăzeci de ani în curierat, de la biroul de relații cu clienții până la scaunul de director. "
                    "Conduc compania, construiesc software-ul și coordonez echipele care țin coletele în mișcare.",
            "cta": "Lucrează cu mine",
            "cv": "Descarcă CV-ul",
            "portrait_alt": "Portretul lui Marius Teler",
            "tracking_label": "Cariera, povestită ca fișa de urmărire a unui colet",
            "tracking_id": "Nr. urmărire MT2006",
            "tracking_chip": "În tranzit",
            "steps": [
                ["Preluat", "Inttel Connect, 2006"],
                ["Sortat", "Nemo Express, 2008–2022"],
                ["Transferat", "Colete Online, Innoship"],
                ["În livrare", "DSC Dragon Star, acum"],
            ],
            "ledger_label": "Cariera în cifre",
            "ledger": [
                ["Ani în IT", 20, ""],
                ["Ani în curierat", 18, "+"],
                ["Roluri, de la birou la director", 7, ""],
                ["Companii de curierat", 4, ""],
            ],
            "marquee_label": "Unelte și domenii cu care lucrez",
            "marquee_extra": ["Raportare SQL", "Rutare pe hub-uri", "Fluxuri POD", "Migrare de date", "Analize curieri"],
        },
        "about": {
            "kicker": "Despre",
            "statement": "Am învățat curieratul din interior: am răspuns la reclamații, am scanat POD-uri, am condus "
                         "suportul clienți, am implementat software nou. Astăzi conduc compania și încă scriu codul "
                         "care o măsoară.",
            "paragraphs": [
                "Am intrat la Nemo Express în 2008, la biroul de reclamații, și am rămas paisprezece ani: "
                "coordonare POD, conducerea suportului clienți, management de proiect și, în final, CIO. "
                "Pe drum am implementat Live Agent, Courier Manager și call center-ul Mediatel și am mutat ani "
                "întregi de date din sistemul vechi.",
                "Apoi am lucrat de partea platformelor de livrare, la Colete Online și Innoship. Din 2024 sunt "
                "Director Executiv la DSC Dragon Star Curier, cu IT-ul și dezvoltarea în subordine. Zilele mele se "
                "împart între conducere și cod: administrez afacerea și livrez uneltele interne care fac operațiunea "
                "măsurabilă.",
            ],
            "facts": [
                ["Locație", "Chiajna, București"],
                ["În prezent", "Director Executiv, DSC Dragon Star Curier"],
                ["Lucrez cu", "Python, Flask, HTMX, PostgreSQL"],
                ["Limbi", "Română, engleză (C1)"],
            ],
        },
        "journey": {
            "kicker": "Traseu",
            "title": "Un traseu de 20 de ani prin industria de curierat",
            "count": "din {n} opriri",
            "stops": [
                {"when": "2006–2008", "role": "Administrator de rețea", "co": "Inttel Connect",
                 "text": "Administrarea rețelelor locale: instalări, depanare și suport pentru clienți. "
                         "Primul job în care să repar lucruri era chiar jobul."},
                {"when": "2008–2019", "role": "Suport clienți, POD și operațiuni", "co": "Nemo Express",
                 "text": "Am început la biroul de reclamații, am coordonat echipa de scanare POD și arhiva, apoi am "
                         "condus suportul clienți: proceduri, angajări, raportare. Am implementat Live Agent."},
                {"when": "2019–2021", "role": "Manager de proiect", "co": "Nemo Express",
                 "text": "Am condus implementarea Courier Manager: obiective, părți implicate și furnizori, "
                         "personalizare și migrarea anilor de date din baza veche."},
                {"when": "2021–2022", "role": "Chief Information Officer", "co": "Nemo Express",
                 "text": "Am condus echipa de IT și dezvoltare, platforma de curierat și call center-ul Mediatel, "
                         "cu sistemele aliniate la obiectivele companiei."},
                {"when": "2022–2023", "role": "IT și operațiuni", "co": "Colete Online",
                 "text": "IT și operațiuni pentru o platformă online de comandă curierat: industria văzută din "
                         "partea de marketplace."},
                {"when": "2023–2024", "role": "IT și operațiuni", "co": "Innoship",
                 "text": "IT și operațiuni pentru o platformă de livrare multi-curier, care conectează expeditorii "
                         "la mai mulți curieri deodată."},
                {"when": "2024–prezent", "role": "Director Executiv", "co": "DSC Dragon Star Curier",
                 "text": "Conduc compania, cu IT-ul și dezvoltarea în subordine. Am construit DSC-Utils, platforma "
                         "internă pentru validări, rutare pe hub-uri și analize de curieri, și noul site al "
                         "companiei."},
            ],
        },
        "projects": {
            "kicker": "Proiecte",
            "title": "Ce am construit",
            "intro": "Site-uri și aplicații gândite și construite de mine, pentru DSC și pentru alte firme.",
            "status": {"live": "Live", "testing": "În testare", "internal": "Intern"},
            "visit": "Vezi site-ul",
            "preview_label": "Captură de ecran cu {name}",
            "items": {
                "dsc": {
                    "name": "Site-ul Dragon Star Curier",
                    "kind": "Site de companie, 2026",
                    "text": "Noul site public al DSC, reconstruit pe CMS-ul PHP existent: o hartă animată a rețelei "
                            "cu cele 5 hub-uri și toate agențiile, un panou pe prima pagină pentru urmărire, "
                            "trimitere și calcul de tarif, comandă online cu eticheta AWB trimisă pe email, pagina "
                            "indicelui de carburant, blog și o pagină SEO pentru fiecare agenție. Fiecare bloc rămâne "
                            "editabil din admin.",
                },
                "servicehub": {
                    "name": "ServiceHub",
                    "kind": "Software pentru service-uri auto, 2026",
                    "text": "Aplicație multi-firmă de management pentru service-uri auto, cu datele fiecărei firme "
                            "izolate la nivel de ORM. Devize și comenzi pe un board Kanban, programări, clienți și "
                            "mașini, stoc de piese, facturare cu transmitere în RO e-Factura (ANAF), documente PDF, "
                            "email prin Mailgun și remindere pentru ITP, RCA și revizii.",
                    "visual": {"columns": ["Nou", "În lucru", "Așteaptă piese", "Gata"],
                               "cards": ["Plăcuțe frână", "Revizie ulei", "Diagnoză", "Încărcare A/C", "Distribuție"]},
                },
                "flota": {
                    "name": "Flota DSC",
                    "kind": "Management de flotă, 2025–2026",
                    "text": "Managementul flotei pentru o companie de curierat: vehicule, șoferi și atribuiri, "
                            "documente cu alerte de expirare (ITP, asigurări, permise), service și mentenanță, "
                            "carburant și costuri operaționale, reguli de notificare și exporturi Excel sau PDF. "
                            "O aplicație Flask pe straturi, cu peste 100 de endpoint-uri API.",
                    "visual": {"head": ["Vehicul", "ITP", "RCA"],
                               "rows": [["Duba 01", ["în 12 zile", "warn"], ["valabil", "ok"]],
                                        ["Duba 02", ["valabil", "ok"], ["în 4 zile", "alert"]],
                                        ["Camion 03", ["valabil", "ok"], ["valabil", "ok"]]],
                               "note": "2 documente expiră luna aceasta"},
                },
                "new4you": {
                    "name": "New4you.ro",
                    "kind": "Magazin online, 2026",
                    "text": "Am mutat un magazin de haine cu licență pentru copii din OpenCart 2.3 în WooCommerce, "
                            "cu o temă proprie. Migrarea e automată și se poate rula oricând din nou: produse și "
                            "variante, clienți cu parolele lor de acum, istoricul comenzilor și redirecționări 301 "
                            "pentru fiecare adresă veche. Plus fluxul de retragere din contract cerut de lege.",
                },
                "willy": {
                    "name": "Willy Car Service",
                    "kind": "Site de prezentare, 2026",
                    "text": "Site de prezentare pentru un service auto din Domnești: servicii, galerie, echipă, "
                            "anunțuri de angajare, hartă și contact, cu butonul de apel mereu la un tap distanță "
                            "pe telefon.",
                },
            },
            "inhouse_title": "Și uneltele pe care le vede doar DSC",
            "inhouse_intro": "Cea mai mare parte din codul meu rulează în interiorul companiei, pe DSC-Utils și în jurul lui.",
            "inhouse": [
                ["Dashboard de statistici", "Volume, statusuri și KPI-uri pe hub și stație, într-un singur loc pentru conducere."],
                ["Analiza curierilor", "Performanța de livrare pe fiecare curier, ca discuțiile să pornească de la cifre."],
                ["Campanii de notificare", "Emailuri personalizate cu atașament Word către toți clienții, prin Mailgun, cu arhivă și raport de livrare."],
                ["Validarea deconturilor", "Potrivește deconturile de ramburs cu depunerile bancare, automat și manual."],
                ["Rutare pe hub-uri și zone", "Trimite fiecare expediție la hub-ul potrivit și leagă fiecare localitate de o zonă de livrare."],
                ["Clienți pierduți", "Găsește clienții care nu mai trimit colete și de când."],
                ["Colete neidentificate", "Un registru cu poze pentru coletele fără etichetă lizibilă, până își găsesc proprietarul."],
            ],
        },
        "expertise": {
            "kicker": "Expertiză",
            "title": "Ce aduc în echipă",
            "areas": [
                {"title": "Conducere", "line": "Construiesc echipe care merg bine și fără mine în cameră.",
                 "points": ["Echipe de IT și dezvoltare", "Obiective de proiect și părți implicate",
                            "Operațiuni de suport clienți", "Angajări și evaluări de performanță"]},
                {"title": "Tehnologie", "line": "Software care transformă operațiunile zilnice în cifre pe care poți acționa.",
                 "points": ["Python, Flask, HTMX", "PostgreSQL și raportare SQL", "PHP, WordPress, WooCommerce",
                            "Courier Manager, Mediatel, Live Agent"]},
                {"title": "Operațiuni de curierat", "line": "Fiecare pas al unui colet, de la preluare la confirmarea livrării.",
                 "points": ["Operațiuni de curierat cap-coadă", "Fluxuri POD și arhivă",
                            "Migrare de date între platforme", "Rutare pe hub-uri și analize"]},
            ],
        },
        "contact": {
            "kicker": "Contact",
            "title": "Să ducem lucrurile mai departe.",
            "lead": "Sunt deschis la consultanță pe IT pentru curierat, parteneriate software și roluri de conducere. "
                    "Răspund în 24 de ore, de obicei mai repede.",
            "keys": {"email": "Email", "phone": "Telefon", "location": "Locație", "github": "GitHub"},
            "location": "Chiajna, București",
            "copy_label": "Copiază adresa de email", "copied": "Copiat", "copy_fallback": "Apasă Ctrl+C",
            "form_title": "Trimite un mesaj",
            "name": "Numele tău", "email": "Email", "message": "Cu ce te pot ajuta?",
            "submit": "Trimite mesajul", "sending": "Se trimite",
            "success_title": "Mulțumesc, mesajul a fost livrat.",
            "success_text": "Îți răspund în 24 de ore, de obicei mai repede.",
            "error_title": "Mesajul nu a plecat.",
            "error_text": "Te rog să îmi scrii direct la",
        },
        "footer": {"elsewhere": "În altă parte", "email": "Email", "cv": "CV", "top": "Înapoi sus"},
        "notfound": {
            "title": "Pagină negăsită, teler.net",
            "heading": "Adresa asta nu e pe traseu.",
            "text": "Pagina s-a mutat sau linkul are o greșeală. Pe prima pagină găsești tot ce e pe site.",
            "cta": "Mergi la prima pagină",
        },
    },
}


def get_content(lang: str) -> dict:
    return CONTENT.get(lang, CONTENT[DEFAULT_LANG])
