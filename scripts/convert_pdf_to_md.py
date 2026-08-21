"""Convert a PDF file to a Markdown file using PyMuPDF."""

import fitz  # PyMuPDF
import re
import sys

def convert_pdf_to_md(pdf_path: str, md_path: str) -> None:
    doc = fitz.open(pdf_path)
    lines = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if not text.strip():
            continue
        if page_num > 0:
            lines.append("\n---\n")
        for line in text.split("\n"):
            if line.strip():
                lines.append(line.rstrip())
            else:
                lines.append("")

    doc.close()

    raw = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", raw).strip()

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(cleaned + "\n")

    print(f"Conversion complete! Output: {md_path}")

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    md_path = sys.argv[2]
    convert_pdf_to_md(pdf_path, md_path)
