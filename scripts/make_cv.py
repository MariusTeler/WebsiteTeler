"""Render the CV (EN + RO) from templates/cv.html to PDF with headless Chromium.

Usage:
    python3 scripts/make_cv.py      # any Python with the app requirements + playwright; starts a throwaway server
Needs: pip install playwright && playwright install chromium (dev only, not in requirements.txt).
Edit the text in cv_content.py, then rerun this script.
"""
import socket
import sys
import threading
from pathlib import Path

from werkzeug.serving import make_server

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import CV_FILES, create_app  # noqa: E402


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> None:
    from playwright.sync_api import sync_playwright

    port = free_port()
    server = make_server("127.0.0.1", port, create_app())
    threading.Thread(target=server.serve_forever, daemon=True).start()
    out_dir = ROOT / "static" / "files"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            for lang, (filename, _) in CV_FILES.items():
                page.goto(f"http://127.0.0.1:{port}/cv/preview?lang={lang}", wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                target = out_dir / filename
                page.pdf(path=str(target), format="A4", print_background=True, prefer_css_page_size=True)
                print(f"{lang}: {target.relative_to(ROOT)} ({target.stat().st_size // 1024} KB)")
            browser.close()
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
