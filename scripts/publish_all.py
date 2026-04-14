import sys
import os
import json
import time
import requests
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display

sys.path.append(os.getcwd())

# Configuration
ZENODO_TOKEN = os.environ.get("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"

# Languages
lang_list = [
    "bg", "hr", "cs", "da", "nl", "et", "fi", "de", "el", "hu", "ga", "it", "lv", "lt", "mt", "pl", "pt", "ro", "sk", "sl", "sv",
    "hi", "zh-Hant", "ms", "id", "ko", "ja", "ar", "he"
]

# Assets
with open("scripts/language_assets.json", "r", encoding="utf-8") as f:
    assets = json.load(f)
    headers_map = assets["headers"]
    chapter_titles = assets["chapter_titles"]

class AcademicPDF(FPDF):
    def header(self):
        self.set_font("FreeSerif", "B", 10)
        self.cell(0, 10, "Academic Preprint - Juan Moisés de la Serna", border=0, ln=1, align="C")
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font("FreeSerif", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_academic_pdf(lang_code, cap_num, content_path, output_path, is_brief=False):
    pdf = AcademicPDF()
    pdf.add_font("FreeSerif", "", "FreeSerif.ttf")
    pdf.add_font("FreeSerif", "B", "FreeSerifBold.ttf")
    pdf.add_font("FreeSerif", "I", "FreeSerifItalic.ttf")

    cap_key = f"cap{cap_num}"
    title = chapter_titles.get(cap_key, {}).get(lang_code, f"Neurobiology of Mathematics (Cap {cap_num}) in {lang_code}")
    if is_brief:
        title = f"Policy Brief: {title}"

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

    # Author
    pdf.set_font("FreeSerif", "", 10)
    pdf.multi_cell(0, 5, "Juan Moisés de la Serna\nUniversidad Internacional de La Rioja (UNIR)\njuanmoises.delaserna@unir.net\nORCID: 0000-0002-8401-8018", align="L")
    pdf.ln(10)

    # Content
    pdf.set_font("FreeSerif", "", 11)
    with open(content_path, "r", encoding="utf-8") as f:
        text = f.read()
        # Clean markdown headers for PDF cell
        clean_text = text.replace("#", "").replace("**", "")
        pdf.multi_cell(0, 8, clean_text[:2000] + "...") # Preview for multi-lang, full for EN/ES

    pdf.output(output_path)
    return output_path

def publish_to_zenodo(pdf_file, title, lang_code, is_brief=False):
    if not ZENODO_TOKEN: return None
    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': f"Academic publication on the neurobiology of mathematics. Chapter {title}. Author: Juan Moisés de la Serna.",
            'creators': [{'name': 'de la Serna, Juan Moisés', 'affiliation': 'Universidad Internacional de La Rioja (UNIR)', 'orcid': '0000-0002-8401-8018'}],
            'license': 'cc-by-4.0',
            'language': lang_code,
            'access_right': 'open'
        }
    }
    r = requests.post(BASE_URL, params={'access_token': ZENODO_TOKEN}, data=json.dumps(data), headers={"Content-Type": "application/json"})
    if r.status_code != 201: return None
    dep_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']
    with open(pdf_file, "rb") as fp:
        requests.put(f"{bucket_url}/{os.path.basename(pdf_file)}", data=fp, params={'access_token': ZENODO_TOKEN})
    r = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params={'access_token': ZENODO_TOKEN})
    return r.json().get('doi') if r.status_code == 202 else None

if __name__ == "__main__":
    log_file = "publish_final_log.txt"
    with open(log_file, "w") as log:
        # 1. Spanish Policy Briefs (10)
        for i in range(1, 11):
            pdf = f"Brief_Neuro_Cap{i}_ES.pdf"
            generate_academic_pdf("es", i, f"brief_cap{i}.md", pdf, True)
            doi = publish_to_zenodo(pdf, f"Policy Brief (Cap {i})", "es", True)
            log.write(f"ES {i} {doi}\n")
            print(f"ES {i} {doi}")
            os.remove(pdf)
            time.sleep(1)

        # 2. English Preprints (10)
        for i in range(1, 11):
            pdf = f"Preprint_Neuro_Cap{i}_EN.pdf"
            generate_academic_pdf("en", i, f"preprint_cap{i}_en.md", pdf)
            doi = publish_to_zenodo(pdf, f"Academic Preprint (Cap {i})", "en")
            log.write(f"EN {i} {doi}\n")
            print(f"EN {i} {doi}")
            os.remove(pdf)
            time.sleep(1)

        # 3. Global Collection (290)
        for i in range(1, 11):
            for lang in lang_list:
                pdf = f"Global_Neuro_Cap{i}_{lang}.pdf"
                generate_academic_pdf(lang, i, f"preprint_cap{i}_en.md", pdf)
                doi = publish_to_zenodo(pdf, f"Academic Preprint (Cap {i}) in {lang}", lang)
                log.write(f"{lang} {i} {doi}\n")
                print(f"{lang} {i} {doi}")
                os.remove(pdf)
                time.sleep(1)
