import os
import re
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("LiberationSerif", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def markdown_to_pdf(md_filepath, pdf_filepath):
    with open(md_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(20, 20, 20)

    # Register Fonts
    font_path = "/usr/share/fonts/truetype/liberation/"
    pdf.add_font("LiberationSerif", "", os.path.join(font_path, "LiberationSerif-Regular.ttf"))
    pdf.add_font("LiberationSerif", "B", os.path.join(font_path, "LiberationSerif-Bold.ttf"))
    pdf.add_font("LiberationSerif", "I", os.path.join(font_path, "LiberationSerif-Italic.ttf"))
    pdf.add_font("LiberationSerif", "BI", os.path.join(font_path, "LiberationSerif-BoldItalic.ttf"))

    pdf.add_page()

    # Use a fixed width for cells to avoid "0" width issues
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

def main():
    preprints_dir = "preprints"
    topics_map = {
        "Chapter_1_Instinto_Numerico.md": "Instinto_Numerico",
        "Chapter_2_Geografia_Calculo.md": "Geografia_Calculo",
        "Chapter_3_Bloques_Ecuaciones.md": "Bloques_Ecuaciones",
        "Chapter_4_Duelo_Cerebral.md": "Duelo_Cerebral",
        "Chapter_5_Atajo_Memoria.md": "Atajo_Memoria",
        "Chapter_6_Panico_Numeros.md": "Panico_Numeros",
        "Chapter_7_Cerebro_Desconectado.md": "Cerebro_Desconectado",
        "Chapter_8_Gimnasio_Mental.md": "Gimnasio_Mental",
        "Chapter_9_Anatomia_Genio.md": "Anatomia_Genio",
        "Chapter_10_Sinfonia_Neuronal.md": "Sinfonia_Neuronal"
    }

    for filename, topic in topics_map.items():
        md_path = os.path.join(preprints_dir, filename)
        if os.path.exists(md_path):
            pdf_filename = f"Preprint_Neuro_{topic}_JuanMoisésdelaSerna.pdf"
            pdf_path = os.path.join(preprints_dir, pdf_filename)
            print(f"Generating {pdf_path}...")
            markdown_to_pdf(md_path, pdf_path)

if __name__ == "__main__":
    main()
