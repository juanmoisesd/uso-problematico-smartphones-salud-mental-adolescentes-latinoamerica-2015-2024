import os
import glob
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class ManuscriptPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('LiberationSerif', 'I', 9)
            self.cell(0, 10, 'Neuroscience of Mathematics Collection - Juan Moisés de la Serna', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def footer(self):
        self.set_y(-15)
        self.set_font('LiberationSerif', 'I', 9)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def clean_markdown(text):
    # Remove Markdown links: [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove bold/italic markers: **text** or *text* -> text
    text = text.replace('***', '').replace('**', '').replace('*', '')
    return text

def create_pdf(markdown_path, output_path, is_en=True):
    pdf = ManuscriptPDF()

    font_path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
    font_bold_path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
    font_italic_path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

    pdf.add_font("LiberationSerif", "", font_path)
    pdf.add_font("LiberationSerif", "B", font_bold_path)
    pdf.add_font("LiberationSerif", "I", font_italic_path)

    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)

    with open(markdown_path, 'r', encoding='utf-8') as f:
        text_content = f.read()

    lines = text_content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue

        if line.startswith("# "):
            pdf.set_font("LiberationSerif", "B", 18)
            text = clean_markdown(line[2:])
            pdf.multi_cell(160, 10, text, align='C')
            pdf.ln(5)
        elif line.startswith("## "):
            pdf.set_font("LiberationSerif", "B", 14)
            text = clean_markdown(line[3:])
            pdf.ln(4)
            pdf.multi_cell(160, 8, text)
            pdf.ln(2)
        elif line.startswith("### "):
            pdf.set_font("LiberationSerif", "B", 12)
            text = clean_markdown(line[4:])
            pdf.multi_cell(160, 7, text)
            pdf.ln(1)
        else:
            pdf.set_font("LiberationSerif", "", 11)
            text = clean_markdown(line)
            if line.startswith("- ") or (len(line) > 2 and line[0].isdigit() and line[1] == '.'):
                 pdf.multi_cell(160, 6, text)
            else:
                 pdf.multi_cell(160, 6, text, align='J')

    pdf.output(output_path)

if __name__ == "__main__":
    es_manuscripts = glob.glob("preprints/manuscripts/*.md")
    os.makedirs("preprints/pdfs", exist_ok=True)
    for m_path in sorted(es_manuscripts):
        filename = os.path.basename(m_path)
        pdf_name = f"Preprint_Neuro_{filename.replace('.md', '')}_JuanMoisesdelaSerna.pdf"
        pdf_path = os.path.join("preprints/pdfs", pdf_name)
        print(f"Generating Spanish: {pdf_path}...")
        create_pdf(m_path, pdf_path, is_en=False)

    en_manuscripts = glob.glob("preprints/manuscripts_en/*.md")
    os.makedirs("preprints/pdfs_en", exist_ok=True)
    for m_path in sorted(en_manuscripts):
        filename = os.path.basename(m_path)
        pdf_name = f"Preprint_Neuro_{filename.replace('.md', '')}_JuanMoisesdelaSerna.pdf"
        pdf_path = os.path.join("preprints/pdfs_en", pdf_name)
        print(f"Generating English: {pdf_path}...")
        create_pdf(m_path, pdf_path, is_en=True)
