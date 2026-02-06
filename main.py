"""Main Logic for PDF AI Prep."""


import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def add_footer_to_pdf(input_path: str, output_path: str) -> None:
    """Add Footer with filename and page number to each page of the PDF."""
    filename = Path(input_path).name
    reader = PdfReader(input_path)
    writer = PdfWriter()
    page_count = len(reader.pages)

    print(f"Processing '{filename}' with {page_count} pages...")
    for page_num, page in enumerate(reader.pages, start=1):

        # Create footer overlay
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        footer_text = f"Source: {filename} | Page {page_num} of {page_count}"
        can.drawString(5, 5, footer_text)
        can.save()

        # Merge footer with page
        packet.seek(0)
        footer_pdf = PdfReader(packet)
        page.merge_page(footer_pdf.pages[0])
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    input_pdf = "example.pdf"
    output_pdf = "output.pdf"
    add_footer_to_pdf(input_pdf, output_pdf)
