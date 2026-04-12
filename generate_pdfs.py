import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PolicyBriefPDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 10, 'Policy Brief - Neurobiología de las Matemáticas', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def markdown_to_pdf(md_file, pdf_file):
    if not os.path.exists(md_file):
        return
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    pdf = PolicyBriefPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
    pdf.add_font('DejaVu', 'I', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf')

    pdf.add_page()

    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue

        w = pdf.epw

        if line.startswith('###'):
            pdf.set_font('DejaVu', 'B', 14)
            text = line.replace('###', '').strip()
            pdf.multi_cell(w, 10, text)
            pdf.ln(2)
        elif line.startswith('**') and line.endswith('**'):
            pdf.set_font('DejaVu', 'B', 12)
            text = line.replace('**', '').strip()
            pdf.multi_cell(w, 8, text)
        elif line.startswith('*   '):
            pdf.set_font('DejaVu', '', 11)
            text = '• ' + line[4:].strip()
            pdf.multi_cell(w, 7, text)
        elif re.match(r'^\d+\.', line):
            pdf.set_font('DejaVu', '', 11)
            pdf.multi_cell(w, 7, line)
        else:
            pdf.set_font('DejaVu', '', 11)
            text = line.replace('**', '')
            pdf.multi_cell(w, 7, text)

    pdf.output(pdf_file)

def main():
    chapters = {
        1: "Instinto_Numerico",
        2: "Geografia_Calculo",
        3: "Bloques_Ecuaciones",
        4: "Duelo_Cerebral",
        5: "Atajo_Memoria",
        6: "Amigdala_Panico",
        7: "Cerebro_Desconectado",
        8: "Gimnasio_Mental",
        9: "Anatomia_Genio",
        10: "Sinfonia_Neuronal"
    }

    for i in range(1, 11):
        md_file = f"brief_cap{i}.md"
        topic = chapters[i]
        pdf_file = f"Preprint_Neuro_{topic}_JuanMoisesdelaSerna.pdf"
        markdown_to_pdf(md_file, pdf_file)

if __name__ == "__main__":
    main()
