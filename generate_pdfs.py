import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PreprintPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load a Unicode font to support Spanish accents
        font_path = "/usr/share/fonts/truetype/liberation/"
        self.add_font("LiberationSerif", "", font_path + "LiberationSerif-Regular.ttf")
        self.add_font("LiberationSerif", "B", font_path + "LiberationSerif-Bold.ttf")
        self.add_font("LiberationSerif", "I", font_path + "LiberationSerif-Italic.ttf")
        self.add_font("LiberationSerif", "BI", font_path + "LiberationSerif-BoldItalic.ttf")
        self.set_font("LiberationSerif", "", 11)

    def header(self):
        if self.page_no() > 1:
            self.set_font("LiberationSerif", "I", 8)
            self.cell(0, 10, self.preprint_title[:100], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("LiberationSerif", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def markdown_to_pdf(md_file, pdf_file):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    pdf = PreprintPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Extract Title
    title_match = re.search(r"^\*\*Título:\*\* (.*)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Preprint"
    pdf.preprint_title = title

    # Cover Page
    pdf.add_page()
    pdf.set_font("LiberationSerif", "B", 16)
    pdf.multi_cell(0, 10, title, align="C")
    pdf.ln(20)

    pdf.set_font("LiberationSerif", "", 12)
    author_info = [
        "Juan Moisés de la Serna",
        "ORCID: https://orcid.org/0000-0002-8401-8018",
        "Universidad Internacional de La Rioja (UNIR)",
        "Email: juanmoises.delaserna@unir.net"
    ]
    for line in author_info:
        pdf.cell(0, 7, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.ln(30)

    # Process content
    lines = content.split("\n")
    skip_header = True
    for line in lines:
        if line.startswith("---"):
            skip_header = False
            continue
        if skip_header:
            continue

        line = line.strip()
        if not line:
            pdf.ln(5)
            continue

        if line.startswith("###"):
            pdf.set_font("LiberationSerif", "B", 13)
            pdf.cell(0, 10, line.replace("###", "").strip(), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
            pdf.set_font("LiberationSerif", "", 11)
        elif line.startswith("**Keywords:**"):
            pdf.set_font("LiberationSerif", "B", 11)
            pdf.write(5, "Keywords: ")
            pdf.set_font("LiberationSerif", "", 11)
            pdf.write(5, line.replace("**Keywords:**", "").strip())
            pdf.ln(10)
        elif line.startswith("**"):
            # Handle bold lines
            pdf.set_font("LiberationSerif", "B", 11)
            pdf.multi_cell(0, 6, line.replace("**", "").strip())
            pdf.set_font("LiberationSerif", "", 11)
            pdf.ln(2)
        elif re.match(r"^\d+\.", line):
            # References
            pdf.set_font("LiberationSerif", "", 9)
            pdf.multi_cell(0, 5, line)
            pdf.ln(1)
        else:
            # Normal paragraph
            pdf.set_font("LiberationSerif", "", 11)
            pdf.multi_cell(0, 6, line)
            pdf.ln(2)

    pdf.output(pdf_file)

if __name__ == "__main__":
    files = [
        ("preprint_01_crisis_replicabilidad.md", "Preprint_Crisis_Replicabilidad_JuanMoisésdelaSerna.pdf"),
        ("preprint_02_validez_dsm.md", "Preprint_Validez_DSM_JuanMoisésdelaSerna.pdf"),
        ("preprint_03_psicofarmacos_psicoterapia.md", "Preprint_Psicofarmacos_Psicoterapia_JuanMoisésdelaSerna.pdf"),
        ("preprint_04_neurodeterminismo.md", "Preprint_Neurodeterminismo_JuanMoisésdelaSerna.pdf"),
        ("preprint_05_terapias_alternativas.md", "Preprint_Terapias_Alternativas_JuanMoisésdelaSerna.pdf"),
        ("preprint_06_inteligencia_genetica.md", "Preprint_Inteligencia_Genetica_JuanMoisésdelaSerna.pdf"),
        ("preprint_07_sesgos_weird.md", "Preprint_Sesgos_WEIRD_JuanMoisésdelaSerna.pdf"),
        ("preprint_08_psicologia_positiva.md", "Preprint_Psicologia_Positiva_JuanMoisésdelaSerna.pdf"),
        ("preprint_09_ia_salud_mental.md", "Preprint_IA_Salud_Mental_JuanMoisésdelaSerna.pdf"),
        ("preprint_10_etica_experimentacion.md", "Preprint_Etica_Experimentacion_JuanMoisésdelaSerna.pdf"),
    ]

    for md, pdf in files:
        print(f"Generating {pdf}...")
        markdown_to_pdf(f"preprints/{md}", f"preprints/{pdf}")
