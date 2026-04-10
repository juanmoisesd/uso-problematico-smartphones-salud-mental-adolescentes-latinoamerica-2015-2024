import json
import os
from fpdf import FPDF

class AcademicPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 10, 'Preprint - Juan Moises de la Serna - Neuroscience Controversy Series', 0, 0, 'R')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_preprint_pdf(topic, metadata_path, output_path):
    pdf = AcademicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cover Page
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.multi_cell(0, 10, topic['title'].encode('latin-1', 'replace').decode('latin-1'), 0, 'C')
    pdf.ln(20)

    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Juan Moises de la Serna', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, 'ORCID: https://orcid.org/0000-0002-8401-8018', 0, 1, 'C')
    pdf.cell(0, 7, 'University International of La Rioja (UNIR)', 0, 1, 'C')
    pdf.cell(0, 7, 'juanmoises.delaserna@unir.net', 0, 1, 'C')
    pdf.ln(20)

    # Abstract on cover
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Abstract', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 7, topic['abstract'].encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, f"Keywords: {', '.join(topic['keywords'])}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')

    # Main Content
    draft_file = f"preprints/{topic['id']}_draft.txt"
    if not os.path.exists(draft_file):
        return

    with open(draft_file, 'r') as f:
        lines = f.readlines()

    pdf.add_page()
    pdf.set_font('Helvetica', '', 11)

    for line in lines:
        # Replace non-latin-1 characters
        clean_line = line.strip().replace('—', '-').replace('–', '-').replace('’', "'").replace('“', '"').replace('”', '"')
        clean_line = clean_line.encode('latin-1', 'replace').decode('latin-1')

        if line.startswith('# '): continue
        if line.startswith('**Abstract:**'): continue
        if line.startswith('**Keywords:**'): continue

        if line.startswith('## '):
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 10, clean_line.replace('## ', ''), 0, 1, 'L')
            pdf.set_font('Helvetica', '', 11)
        else:
            pdf.multi_cell(0, 7, clean_line)
            if clean_line: pdf.ln(2)

    # Bibliography
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'References', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 9)

    bib_file = f"metadata/{topic['id']}_bib.txt"
    if os.path.exists(bib_file):
        with open(bib_file, 'r') as f:
            bib_lines = f.readlines()

        for bib_line in bib_lines:
            clean_bib = bib_line.strip().replace('—', '-').replace('–', '-').replace('’', "'").replace('“', '"').replace('”', '"')
            pdf.multi_cell(0, 4, clean_bib.encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln(1)

    pdf.output(output_path)

if __name__ == "__main__":
    with open('metadata/preprints_metadata.json', 'r') as f:
        topics = json.load(f)

    for topic in topics:
        safe_title = topic['id']
        output_filename = f"preprints/Preprint_Neuro_{safe_title}_JuanMoisesdelaSerna.pdf"
        create_preprint_pdf(topic, 'metadata', output_filename)
        print(f"Generated: {output_filename}")
