"""Main Logic for PDF AI Prep."""


import argparse
import io
import os
import sys
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

    print(f"Adding footer to '{filename}' with {page_count} pages")
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
    """Merge PDFs and add filename bookmarks."""
    writer = PdfWriter()
    print(f"Merging {pdf_files} to single PDF : {output_path}")
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        start_page = len(writer.pages)

        # Add pages
        for page in reader.pages:
            writer.add_page(page)

        # Add bookmark for this file
        filename = Path(pdf_file).stem.replace("stamped_", "")
        bookmark_text = f"{filename} (pages {start_page + 1}-{start_page + len(reader.pages)})"
        writer.add_outline_item(bookmark_text, start_page)

    with open(output_path, "wb") as f:
        writer.write(f)


def process_pdfs(input_files, output_path):
    """Process a series of PDFs by adding footers then merging them."""
    stamped_files = []

    print("Adding footers")
    for pdf_file in input_files:
        stamped_path = f"stamped_{Path(pdf_file).name}"
        add_footer_to_pdf(pdf_file, stamped_path)
        stamped_files.append(stamped_path)
        print(f"Stamped {pdf_file}")

    print(f"Merging {len(stamped_files)} PDFs")
    merge_pdfs_with_bookmarks(stamped_files, output_path)
    print(f"Created: {output_path}")

    print("Cleaning up temp stamp files")
    for stamped_file in stamped_files:
        os.remove(stamped_file)
    print("Complete!")


def process_folder(folder_path, output_path):
    """Process all PDFs in a folder."""
    pdf_files = [str(p) for p in Path(folder_path).glob("*.pdf")]
    print(f"Processing folder: {folder_path} with pdf count {len(pdf_files)} files")
    process_pdfs(pdf_files, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description='Process and merge PDFs from a folder with footers and bookmarks',
    )
    parser.add_argument(
        'folder',
        help='Path to folder containing PDF files',
    )

    args = parser.parse_args()
    if not args.folder:
        print("Error: Folder path is required.")
        parser.print_help()
        sys.exit(1)

    folder_path = Path(args.folder)

    # Generate output filename
    output_name = f"{folder_path.name}_combined.pdf"
    output_path = Path(folder_path) / output_name

    # Process the folder
    process_folder(args.folder, output_path)
