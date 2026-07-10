from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "public" / "assets" / "ce-logic-logo.png"
OUT_DIR = ROOT / "public" / "assets" / "resources"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DOCS = [
    {
        "file": "natcon-2026-full-program-mock.pdf",
        "title": "Full Program",
        "subtitle": "18th CE-Logic National Conference",
        "body": [
            "This mock PDF previews the two-day conference program for July 30-31, 2026.",
            "Includes keynote address, expert sessions, panel discussion, and technology showcase coverage.",
        ],
    },
    {
        "file": "natcon-2026-plai-endorsement-mock.pdf",
        "title": "PLAI Endorsement Letter",
        "subtitle": "Philippine Librarians Association, Inc.",
        "body": [
            "This mock PDF stands in for the official PLAI endorsement letter.",
            "Final signed copy will be published before the conference.",
        ],
    },
    {
        "file": "natcon-2026-partner-brochures-mock.pdf",
        "title": "Partner Resources (Brochures)",
        "subtitle": "Sponsor and partner collateral",
        "body": [
            "This mock PDF bundles sample partner brochure pages for preview purposes.",
            "Production brochures will be linked from the Partners section.",
        ],
    },
    {
        "file": "natcon-2026-presentation-decks-mock.pdf",
        "title": "Presentation Decks",
        "subtitle": "Speaker and partner slide materials",
        "body": [
            "This mock PDF represents downloadable presentation decks from the program.",
            "Final decks will be released after event-day sessions.",
        ],
    },
]


def build_pdf(doc: dict) -> None:
    pdf = FPDF(unit="mm", format="letter")
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    pdf.image(str(LOGO), x=20, y=18, w=48)
    pdf.set_y(42)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(200, 32, 40)
    pdf.cell(0, 12, "MOCK DOCUMENT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 80, 140)
    pdf.cell(0, 10, doc["title"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, doc["subtitle"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(245, 184, 0)
    pdf.set_line_width(0.8)
    y = pdf.get_y()
    pdf.line(20, y, 196, y)
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(10, 36, 60)
    pdf.cell(0, 8, "CE-Logic National Conference 2026", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    for line in doc["body"]:
        pdf.multi_cell(0, 6, line)
        pdf.ln(2)
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0,
        5,
        "For demonstration only. This is not an official conference document. Replace with final materials before publication.",
    )
    pdf.output(str(OUT_DIR / doc["file"]))


for item in DOCS:
    build_pdf(item)
    print(f"Wrote {item['file']}")