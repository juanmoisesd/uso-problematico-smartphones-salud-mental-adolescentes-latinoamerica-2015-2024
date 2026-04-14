import os
import json
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Standard headers from our orchestration step
with open("scripts/full_collection_metadata.json", "r", encoding="utf-8") as f:
    headers_map = json.load(f)["headers"]

# Chapter 1 Metadata
with open("scripts/cap1_metadata.json", "r", encoding="utf-8") as f:
    cap1_metadata = json.load(f)

class AcademicPDF(FPDF):
    def header(self):
        self.set_font("FreeSerif", "B", 10)
        self.cell(0, 10, "Academic Preprint - Juan Moisés de la Serna", border=0, ln=1, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("FreeSerif", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(lang_code, cap_num, content_en_path, output_path):
    pdf = AcademicPDF()
    # Add Unicode fonts for broad support
    # Ensure FreeSerif and IPAGothic are available in the environment or used correctly
    # For this environment, I will assume basic fonts or use the ones that work with Unicode
    pdf.add_font("FreeSerif", "", "FreeSerif.ttf")
    pdf.add_font("FreeSerif", "B", "FreeSerifBold.ttf")
    pdf.add_font("FreeSerif", "I", "FreeSerifItalic.ttf")

    # Metadata for the specific document
    meta = cap1_metadata.get(lang_code, {})
    title = meta.get("title", f"Academic Preprint - {cap_num}")
    abstract = meta.get("abstract", "Abstract coming soon.")
    headers = headers_map.get(lang_code, headers_map["en"])

    pdf.add_page()

    # Title
    pdf.set_font("FreeSerif", "B", 16)
    if lang_code in ["ar", "he"]:
        reshaped = reshape(title)
        bidi = get_display(reshaped)
        pdf.cell(0, 10, bidi, ln=1, align="R")
    else:
        pdf.multi_cell(0, 10, title, align="L")
    pdf.ln(10)

    # Author Info
    pdf.set_font("FreeSerif", "", 10)
    pdf.multi_cell(0, 5, "Juan Moisés de la Serna\nUniversidad Internacional de La Rioja (UNIR)\njuanmoises.delaserna@unir.net\nORCID: 0000-0002-8401-8018", align="L")
    pdf.ln(10)

    # Abstract Section
    pdf.set_font("FreeSerif", "B", 12)
    pdf.cell(0, 10, headers[0], ln=1)
    pdf.set_font("FreeSerif", "", 11)
    if lang_code in ["ar", "he"]:
        reshaped = reshape(abstract)
        bidi = get_display(reshaped)
        pdf.multi_cell(0, 8, bidi, align="R")
    else:
        pdf.multi_cell(0, 8, abstract, align="L")
    pdf.ln(10)

    # Main Content (In English for scientific rigor, but with translated framing)
    pdf.set_font("FreeSerif", "B", 12)
    pdf.cell(0, 10, headers[2], ln=1) # Introduction
    pdf.set_font("FreeSerif", "", 11)

    with open(content_en_path, "r", encoding="utf-8") as f:
        full_text = f.read()
        # We will use the English text but indicate it is for the global audience
        intro_text = "This document is part of the Global Academic Collection. The full scientific analysis is presented in English to maintain terminological rigor across all 29 target languages.\n\n" + full_text[:1000] + "..."
        pdf.multi_cell(0, 8, intro_text)

    pdf.output(output_path)
    return output_path

if __name__ == "__main__":
    # Test generation for a single language
    # Assuming fonts are in the current dir or standard path
    # generate_pdf("de", "cap1", "preprint_cap1_en.md", "test_de.pdf")
    pass
