import os
import re
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("LiberationSerif", "I", 8)
        if self.lang == "en":
            text = f"Page {self.page_no()}"
        elif self.lang == "fr":
            text = f"Page {self.page_no()}"
        else:
            text = f"Página {self.page_no()}"
        self.cell(0, 10, text, align="C")

def markdown_to_pdf(md_filepath, pdf_filepath, lang="es"):
    with open(md_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.lang = lang
    pdf.set_margins(20, 20, 20)

    # Register Fonts
    font_path = "/usr/share/fonts/truetype/liberation/"
    pdf.add_font("LiberationSerif", "", os.path.join(font_path, "LiberationSerif-Regular.ttf"))
    pdf.add_font("LiberationSerif", "B", os.path.join(font_path, "LiberationSerif-Bold.ttf"))
    pdf.add_font("LiberationSerif", "I", os.path.join(font_path, "LiberationSerif-Italic.ttf"))
    pdf.add_font("LiberationSerif", "BI", os.path.join(font_path, "LiberationSerif-BoldItalic.ttf"))

    pdf.add_page()

    cell_width = pdf.w - 2 * pdf.l_margin

    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue

        if line.startswith("# "):
            pdf.set_font("LiberationSerif", "B", 16)
            pdf.multi_cell(cell_width, 10, text=line[2:])
            pdf.ln(5)
        elif line.startswith("### "):
            pdf.set_font("LiberationSerif", "B", 12)
            pdf.multi_cell(cell_width, 8, text=line[4:])
            pdf.ln(2)
        elif line.startswith("**") and line.endswith("**"):
            pdf.set_font("LiberationSerif", "B", 11)
            pdf.multi_cell(cell_width, 6, text=line.strip("*"))
        elif line.startswith("*"):
            pdf.set_font("LiberationSerif", "I", 10)
            pdf.multi_cell(cell_width, 6, text=line.strip("*"))
        else:
            pdf.set_font("LiberationSerif", "", 11)
            clean_line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
            clean_line = re.sub(r"\*(.*?)\*", r"\1", clean_line)
            pdf.multi_cell(cell_width, 6, text=clean_line)
            pdf.ln(2)

    pdf.output(pdf_filepath)

def process_directory(lang):
    preprints_dir = f"preprints/{lang}"
    if not os.path.exists(preprints_dir):
        return

    for filename in os.listdir(preprints_dir):
        if filename.endswith(".md"):
            md_path = os.path.join(preprints_dir, filename)
            topic = filename.replace("Chapter_", "").replace(".md", "")
            topic_clean = topic.split("_", 1)[1] if "_" in topic else topic

            pdf_filename = f"Preprint_Neuro_{topic_clean}_JuanMoisésdelaSerna.pdf"
            pdf_path = os.path.join(preprints_dir, pdf_filename)

            print(f"Generating {pdf_path}...")
            markdown_to_pdf(md_path, pdf_path, lang=lang)

def main():
    process_directory("es")
    process_directory("en")
    process_directory("fr")

if __name__ == "__main__":
    main()
