import os
import glob
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class ManuscriptPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('LiberationSerif', 'I', 8)
            self.cell(0, 10, 'Neurociencia de las Matemáticas - Juan Moisés de la Serna', align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def footer(self):
        self.set_y(-15)
        self.set_font('LiberationSerif', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def create_pdf(markdown_path, output_path):
    pdf = ManuscriptPDF()

    # Load Unicode fonts
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
    font_bold_path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
    font_italic_path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

    pdf.add_font("LiberationSerif", "", font_path)
    pdf.add_font("LiberationSerif", "B", font_bold_path)
    pdf.add_font("LiberationSerif", "I", font_italic_path)

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set margins explicitly to be safe
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)

    with open(markdown_path, 'r', encoding='utf-8') as f:
        text_content = f.read()

    lines = text_content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue

        # Determine font and style
        if line.startswith("# "):
            pdf.set_font("LiberationSerif", "B", 16)
            text = line[2:]
            spacing = 10
        elif line.startswith("## "):
            pdf.set_font("LiberationSerif", "B", 14)
            text = line[3:]
            spacing = 10
        elif line.startswith("### "):
            pdf.set_font("LiberationSerif", "B", 12)
            text = line[4:]
            spacing = 8
        else:
            pdf.set_font("LiberationSerif", "", 11)
            text = line.strip("*")
            spacing = 6

        # Use a safe width (Total A4 width is 210mm, minus 40mm margins = 170mm)
        pdf.multi_cell(170, spacing, text)

    pdf.output(output_path)

if __name__ == "__main__":
    manuscripts = glob.glob("preprints/manuscripts/*.md")
    os.makedirs("preprints/pdfs", exist_ok=True)

    mapping = {
        "Capitulo_1_Instinto_Numerico.md": "Instinto_Numerico",
        "Capitulo_2_Geografia_Calculo.md": "Geografia_Calculo",
        "Capitulo_3_Aprendizaje_Infantil.md": "Aprendizaje_Infantil",
        "Capitulo_4_Duelo_Cerebral.md": "Duelo_Cerebral",
        "Capitulo_5_Memoria_Automatizacion.md": "Memoria_Automatizacion",
        "Capitulo_6_Ansiedad_Matematica.md": "Ansiedad_Matematica",
        "Capitulo_7_Discalculia.md": "Discalculia",
        "Capitulo_8_Gimnasio_Mental.md": "Gimnasio_Mental",
        "Capitulo_9_Anatomia_Genio.md": "Anatomia_Genio",
        "Capitulo_10_Sinfonia_Neuronal.md": "Sinfonia_Neuronal"
    }

    for m_path in sorted(manuscripts):
        filename = os.path.basename(m_path)
        topic = mapping.get(filename, "Topic")
        pdf_name = f"Preprint_Neuro_{topic}_JuanMoisesdelaSerna.pdf"
        pdf_path = os.path.join("preprints/pdfs", pdf_name)
        print(f"Generating {pdf_path}...")
        create_pdf(m_path, pdf_path)
