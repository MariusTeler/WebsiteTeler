"""Content of the downloadable CV (EN and RO), rendered by templates/cv.html.

Regenerate the PDFs after editing:  python3 scripts/make_cv.py
Deliberately left out of the public CV: date of birth, home street address, second phone, Facebook.
"""

CV = {
    "en": {
        "lang": "en",
        "doc_title": "Marius Teler, CV",
        "name": "Marius Teler",
        "full_name": "Teler Marius Adrian",
        "headline": "Executive Director, courier IT and operations",
        "contact": [
            ["Email", "marius.teler@gmail.com", "mailto:marius.teler@gmail.com"],
            ["Phone", "+40 700 64 137", "tel:+4070064137"],
            ["Web", "teler.net", "https://teler.net"],
            ["GitHub", "github.com/MariusTeler", "https://github.com/MariusTeler"],
            ["Location", "Chiajna, Bucharest, Romania", None],
        ],
        "labels": {
            "profile": "Profile", "experience": "Experience", "projects": "Selected projects",
            "skills": "Skills", "languages": "Languages", "education": "Education",
            "other": "Other", "present": "present", "updated": "Updated",
        },
        "updated": "November 2026",
        "profile": (
            "Self-taught executive with 20 years in IT and 18 in the courier industry. I grew from the "
            "complaints desk at Nemo Express to CIO, then worked on the platform side of delivery at Colete "
            "Online and Innoship. Since 2024 I have been Executive Director of DSC Dragon Star Curier, with IT "
            "and Development under my remit. I lead the teams and I also build the software: the in-house "
            "platform, the company website, and products for other businesses."
        ),
        "experience": [
            {"role": "Executive Director", "co": "DSC Dragon Star Curier", "where": "Bucharest",
             "when": "2024 to present",
             "points": [
                 "Direct the company, with IT and Development reporting to me.",
                 "Built DSC-Utils, the in-house platform: cash-on-delivery settlement validation against bank "
                 "deposits, hub routing and zone mapping, hub and courier performance reports, lost-client "
                 "analysis and client notification campaigns through Mailgun.",
                 "Rebuilt the public website on the company CMS: network map with 5 hubs and every agency, "
                 "online booking with an AWB label by email, tracking and pricing panels, a fuel index page "
                 "and an SEO page for each agency.",
                 "Built Flota DSC, the fleet management app: vehicles, drivers, documents with expiry alerts, "
                 "service, fuel and operating costs.",
             ]},
            {"role": "IT and Operations", "co": "Innoship", "where": "Bucharest", "when": "2023 to 2024",
             "points": ["IT and operations for a multi-carrier delivery platform that connects shippers "
                        "to many couriers at once."]},
            {"role": "IT and Operations", "co": "Colete Online", "where": "Bucharest", "when": "2022 to 2023",
             "points": ["IT and operations for an online courier booking platform."]},
            {"role": "Chief Information Officer", "co": "Nemo Express", "where": "Măgurele",
             "when": "Jan 2021 to Sep 2022",
             "points": [
                 "Managed the IT and development team.",
                 "Kept systems and procedures aligned with business goals.",
                 "Implemented and ran the Mediatel call and contact center; ran the Courier Manager postal software.",
             ]},
            {"role": "Project Manager", "co": "Nemo Express", "where": "Măgurele", "when": "Jun 2019 to Jan 2021",
             "points": [
                 "Implemented the Courier Manager software, coordinating internal teams and third parties.",
                 "Defined scope and objectives with all stakeholders and secured technical feasibility and resources.",
                 "Customized the system and migrated the data from the legacy database.",
                 "Managed the development backlog, the project team and reporting to management.",
             ]},
            {"role": "Customer Support Manager and earlier roles", "co": "Nemo Express", "where": "Măgurele",
             "when": "Apr 2008 to 2019",
             "points": [
                 "Customer Support Manager: ran the department day to day, escalations, support policies, "
                 "statistics and reports, hiring and performance reviews. Implemented Live Agent.",
                 "POD Coordinator: led the POD team, scanning procedures and the POD archive database; "
                 "introduced new hardware and software.",
                 "Customer service roles from 2008: complaints handling, inbound calls, account relationships.",
             ]},
            {"role": "Network Manager", "co": "Inttel Connect", "where": "Bucharest", "when": "Jan 2006 to Jan 2008",
             "points": ["Local network management, implementation and troubleshooting; client support."]},
        ],
        "projects": [
            ["ServiceHub", "2026, in testing",
             "Multi-tenant management app for car repair shops: work orders on Kanban, appointments, stock, "
             "invoicing with RO e-Factura (ANAF), reminders."],
            ["New4you.ro", "2026",
             "Online store migrated from OpenCart to WooCommerce with a custom theme, automated data "
             "migration and 301 redirects."],
            ["Willy Car Service", "2026", "Presentation website for a car repair shop in Domnești."],
            ["teler.net", "2026", "This personal website, in English and Romanian."],
        ],
        "skills": [
            ["Leadership", "IT and development teams, project scope and stakeholders, customer support "
                           "operations, hiring and performance reviews"],
            ["Software", "Python, Flask, HTMX, SQLAlchemy, PostgreSQL, SQL reporting, PHP, WordPress and "
                         "WooCommerce, Mailgun, RO e-Factura"],
            ["Courier", "End-to-end operations, POD and archive workflows, hub routing, data migration "
                        "between platforms"],
            ["Tools", "Courier Manager, Mediatel, Live Agent, Qlik Sense, ChronoScan, MS Office"],
        ],
        "languages": [
            ["Romanian", "native"],
            ["English", "C1 listening and reading, B2 writing, B1 speaking"],
        ],
        "education": [
            ["Computer Operator Certificate", "Mihail Sadoveanu High School, Bucharest", "2005"],
            ["High school diploma", "Mihail Sadoveanu High School, Bucharest", "2001 to 2005"],
        ],
        "other": [
            ["Driving licence", "B"],
            ["Interests", "Skiing, rock music, travel, reading, PC gaming"],
        ],
    },
    "ro": {
        "lang": "ro",
        "doc_title": "Marius Teler, CV",
        "name": "Marius Teler",
        "full_name": "Teler Marius Adrian",
        "headline": "Director Executiv, IT și operațiuni în curierat",
        "contact": [
            ["Email", "marius.teler@gmail.com", "mailto:marius.teler@gmail.com"],
            ["Telefon", "+40 700 64 137", "tel:+4070064137"],
            ["Web", "teler.net/ro/", "https://teler.net/ro/"],
            ["GitHub", "github.com/MariusTeler", "https://github.com/MariusTeler"],
            ["Locație", "Chiajna, București, România", None],
        ],
        "labels": {
            "profile": "Profil", "experience": "Experiență", "projects": "Proiecte alese",
            "skills": "Competențe", "languages": "Limbi străine", "education": "Studii",
            "other": "Altele", "present": "prezent", "updated": "Actualizat",
        },
        "updated": "noiembrie 2026",
        "profile": (
            "Manager autodidact, cu 20 de ani în IT și 18 în curierat. Am crescut de la biroul de reclamații "
            "al Nemo Express până la funcția de CIO, apoi am lucrat de partea platformelor de livrare, la Colete "
            "Online și Innoship. Din 2024 sunt Director Executiv la DSC Dragon Star Curier, cu IT-ul și "
            "dezvoltarea în subordine. Conduc echipele și construiesc și software-ul: platforma internă, site-ul "
            "companiei și produse pentru alte firme."
        ),
        "experience": [
            {"role": "Director Executiv", "co": "DSC Dragon Star Curier", "where": "București",
             "when": "2024–prezent",
             "points": [
                 "Conduc compania, cu departamentele de IT și dezvoltare în subordine.",
                 "Am construit DSC-Utils, platforma internă: validarea deconturilor de ramburs față de depunerile "
                 "bancare, rutare pe hub-uri și zone, rapoarte de performanță pe hub-uri și curieri, analiza "
                 "clienților pierduți și campanii de notificare a clienților prin Mailgun.",
                 "Am refăcut site-ul public pe CMS-ul companiei: harta rețelei cu 5 hub-uri și toate agențiile, "
                 "comandă online cu eticheta AWB pe email, panouri de urmărire și calcul tarif, pagina indicelui "
                 "de carburant și o pagină SEO pentru fiecare agenție.",
                 "Am construit Flota DSC, aplicația de management al flotei: vehicule, șoferi, documente cu alerte "
                 "de expirare, service, carburant și costuri operaționale.",
             ]},
            {"role": "IT și operațiuni", "co": "Innoship", "where": "București", "when": "2023–2024",
             "points": ["IT și operațiuni pentru o platformă de livrare multi-curier, care conectează "
                        "expeditorii la mai mulți curieri deodată."]},
            {"role": "IT și operațiuni", "co": "Colete Online", "where": "București", "when": "2022–2023",
             "points": ["IT și operațiuni pentru o platformă online de comandă curierat."]},
            {"role": "Chief Information Officer (CIO)", "co": "Nemo Express", "where": "Măgurele",
             "when": "ian. 2021–sept. 2022",
             "points": [
                 "Am condus echipa de IT și dezvoltare.",
                 "Am aliniat sistemele și procedurile la obiectivele companiei.",
                 "Am implementat și administrat call center-ul Mediatel; am administrat aplicația de curierat Courier Manager.",
             ]},
            {"role": "Manager de proiect", "co": "Nemo Express", "where": "Măgurele", "when": "iun. 2019–ian. 2021",
             "points": [
                 "Am implementat aplicația Courier Manager, coordonând echipele interne și furnizorii externi.",
                 "Am definit obiectivele proiectului cu toate părțile implicate și am asigurat fezabilitatea tehnică și resursele.",
                 "Am personalizat sistemul și am migrat datele din baza de date veche.",
                 "Am gestionat lista de dezvoltări, echipa de proiect și raportarea către conducere.",
             ]},
            {"role": "Manager suport clienți și roluri anterioare", "co": "Nemo Express", "where": "Măgurele",
             "when": "apr. 2008–2019",
             "points": [
                 "Manager suport clienți: activitatea zilnică a departamentului, escaladări, proceduri de suport, "
                 "statistici și rapoarte, angajări și evaluări de performanță. Am implementat Live Agent.",
                 "Coordonator POD: echipa POD, procedurile de scanare și baza de date a arhivei POD; am introdus "
                 "echipamente și software noi.",
                 "Roluri în relații cu clienții din 2008: reclamații, apeluri, relația cu conturile de clienți.",
             ]},
            {"role": "Administrator de rețea", "co": "Inttel Connect", "where": "București", "when": "ian. 2006–ian. 2008",
             "points": ["Administrarea, implementarea și depanarea rețelelor locale; suport pentru clienți."]},
        ],
        "projects": [
            ["ServiceHub", "2026, în testare",
             "Aplicație multi-firmă pentru service-uri auto: comenzi pe Kanban, programări, stoc, facturare "
             "cu RO e-Factura (ANAF), remindere."],
            ["New4you.ro", "2026",
             "Magazin online mutat din OpenCart în WooCommerce, cu temă proprie, migrare automată a datelor "
             "și redirecționări 301."],
            ["Willy Car Service", "2026", "Site de prezentare pentru un service auto din Domnești."],
            ["teler.net", "2026", "Site-ul meu personal, în română și engleză."],
        ],
        "skills": [
            ["Conducere", "Echipe de IT și dezvoltare, obiective de proiect și părți implicate, operațiuni de "
                          "suport clienți, angajări și evaluări de performanță"],
            ["Software", "Python, Flask, HTMX, SQLAlchemy, PostgreSQL, raportare SQL, PHP, WordPress și "
                         "WooCommerce, Mailgun, RO e-Factura"],
            ["Curierat", "Operațiuni cap-coadă, fluxuri POD și arhivă, rutare pe hub-uri, migrare de date "
                         "între platforme"],
            ["Unelte", "Courier Manager, Mediatel, Live Agent, Qlik Sense, ChronoScan, MS Office"],
        ],
        "languages": [
            ["Română", "limba maternă"],
            ["Engleză", "C1 ascultare și citire, B2 scriere, B1 vorbire"],
        ],
        "education": [
            ["Atestat de operator calculator", "Liceul Mihail Sadoveanu, București", "2005"],
            ["Diplomă de liceu", "Liceul Mihail Sadoveanu, București", "2001–2005"],
        ],
        "other": [
            ["Permis de conducere", "categoria B"],
            ["Pasiuni", "Schi, muzică rock, călătorii, lectură, jocuri pe PC"],
        ],
    },
}


def get_cv(lang: str) -> dict:
    return CV.get(lang, CV["en"])
