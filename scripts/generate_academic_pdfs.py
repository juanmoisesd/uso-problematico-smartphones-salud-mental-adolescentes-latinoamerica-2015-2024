import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import arabic_reshaper
from bidi.algorithm import get_display

class MultiLangAcademicPDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'I', 10)
        title = "Academic Preprint - Neurobiology of Mathematics Collection"
        self.cell(0, 10, title, align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | de la Serna, J. M. (2026)', align='C')

def prepare_text(text, lang):
    if lang in ['ar', 'he']:
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    return text

def markdown_to_pdf_v2(md_file, pdf_file, lang):
    if not os.path.exists(md_file):
        return
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    pdf = MultiLangAcademicPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
    pdf.add_font('DejaVu', 'I', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf')
    pdf.add_font('FreeSerif', '', '/usr/share/fonts/truetype/freefont/FreeSerif.ttf')

    if lang in ['ja', 'zh-Hant', 'ko', 'zh']:
        pdf.add_font('CJK', '', '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf')
        main_font = 'CJK'
    elif lang in ['hi', 'ar', 'he']:
        main_font = 'FreeSerif'
    else:
        main_font = 'DejaVu'

    pdf.add_page()
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue
        w = pdf.epw
        processed_line = prepare_text(line, lang)
        if line.startswith('# '):
            pdf.set_font(main_font, 'B' if main_font == 'DejaVu' else '', 18)
            text = processed_line.replace('# ', '').strip()
            pdf.multi_cell(w, 10, text, align='C')
            pdf.ln(5)
        elif 'Juan Moisés de la Serna' in line:
            pdf.set_font(main_font, 'B' if main_font == 'DejaVu' else '', 12)
            pdf.multi_cell(w, 7, processed_line)
        elif line.startswith('## '):
            pdf.set_font(main_font, 'B' if main_font == 'DejaVu' else '', 14)
            text = processed_line.replace('## ', '').strip()
            pdf.multi_cell(w, 8, text)
            pdf.ln(2)
        elif line.startswith('### '):
            pdf.set_font(main_font, 'B' if main_font == 'DejaVu' else '', 12)
            text = processed_line.replace('### ', '').strip()
            pdf.multi_cell(w, 7, text)
        else:
            pdf.set_font(main_font, '', 11)
            text = processed_line.replace('**', '').replace('*', '')
            pdf.multi_cell(w, 6, text, align='R' if lang in ['ar', 'he'] else 'L')
    pdf.output(pdf_file)
