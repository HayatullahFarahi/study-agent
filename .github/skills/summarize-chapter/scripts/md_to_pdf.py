#!/usr/bin/env python3
"""Render a study summary (Markdown) to a styled PDF with WeasyPrint.

Usage: md_to_pdf.py <summary.md> [<output.pdf>]

Images, stylesheets, attachments and file:// links in the Markdown are never fetched, so
content copied from a material cannot pull local files into the PDF.
"""

import sys
from pathlib import Path

CSS = """
body { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; margin: 36px; color: #1a1a1a; line-height: 1.45; }
h1, h2 { color: #2c3e50; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
pre { background: #f4f4f4; padding: 12px; border-radius: 4px; font-size: 0.8em; white-space: pre-wrap; }
code { background: #f0f0f0; padding: 1px 4px; border-radius: 3px; font-family: Menlo, Consolas, monospace; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; vertical-align: top; }
th { background: #eaf0fb; }
blockquote { border-left: 4px solid #aaa; margin-left: 0; padding-left: 12px; color: #555; }
details { margin: 6px 0; }
summary { font-weight: 600; }
"""


def blocking_fetcher():
    def refuse(url, *args, **kwargs):
        raise ValueError(f"external resource blocked: {url}")

    try:
        from weasyprint.urls import (
            URLFetcher,
        )  # WeasyPrint >= 66 expects a URLFetcher instance
    except ImportError:
        return refuse

    class NoFetch(URLFetcher):
        def fetch(self, url, headers=None):
            refuse(url)

    return NoFetch()


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print(__doc__, file=sys.stderr)
        return 2
    md_path = Path(argv[1])
    pdf_path = Path(argv[2]) if len(argv) == 3 else md_path.with_suffix(".pdf")
    if not md_path.is_file():
        print(f"ERROR: Not found: {md_path}", file=sys.stderr)
        return 2
    try:
        import markdown
        from weasyprint import HTML
    except (
        ImportError,
        OSError,
    ) as exc:  # OSError: WeasyPrint's system libraries (Pango) are missing
        print(
            f'MISSING DEPENDENCY: {exc}\nInstall with: "{sys.executable}" -m pip install markdown weasyprint'
            "\nmacOS also needs: brew install pango",
            file=sys.stderr,
        )
        return 3
    body = markdown.markdown(
        md_path.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    HTML(string=html, url_fetcher=blocking_fetcher()).write_pdf(str(pdf_path))
    print(f"PDF saved: {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
