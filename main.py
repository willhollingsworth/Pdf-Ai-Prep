"""Main Logic for PDF AI Prep."""


import io
import os
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


def merge_pdfs_with_bookmarks(pdf_files, output_path):
    """Merge PDFs and add filename bookmarks"""
    writer = PdfWriter()

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        start_page = len(writer.pages)

        # Add pages
        for page in reader.pages:
            writer.add_page(page)

        # Add bookmark for this file
        filename = Path(pdf_file).stem
        bookmark_text = f"{filename} (pages {start_page + 1}-{start_page + len(reader.pages)})"
        writer.add_outline_item(bookmark_text, start_page)

    with open(output_path, "wb") as f:
        writer.write(f)


def process_pdfs(input_files, final_output):
    """Process a series of PDFs."""
    stamped_files = []

    print("Adding footers")
    for pdf_file in input_files:
        stamped_path = f"stamped_{Path(pdf_file).name}"
        add_footer_to_pdf(pdf_file, stamped_path)
        stamped_files.append(stamped_path)
        print(f"Stamped {pdf_file}")

    print(f"Merging {len(stamped_files)} PDFs")
    merge_pdfs_with_bookmarks(stamped_files, final_output)
    print(f"Created: {final_output}")

    print("cleaning up temp files")
    for stamped_file in stamped_files:
        os.remove(stamped_file)

    print("Complete!")


if __name__ == "__main__":

    # example footer
    # input_pdf = "example.pdf"
    # output_pdf = "output.pdf"
    # add_footer_to_pdf(input_pdf, output_pdf)

    # example merge
    # pdf_list = ["example 1.pdf", "example 2.pdf"]
    # output_pdf = "combined_output.pdf"
    # merge_pdfs_with_bookmarks(pdf_list, output_pdf)

    # example process
    pdf_list = ["example 1.pdf", "example 2.pdf"]
    output_pdf = "combined_output.pdf"
    process_pdfs(pdf_list, output_pdf)
