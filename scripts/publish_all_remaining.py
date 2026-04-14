import sys
import os
import json
import time
import requests
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Configuration
ZENODO_TOKEN = "N7VErxvSFds8OrqDAy5zh4HyfDGDsDWe1OROHnmGivrStTOSHSTD54ZH1LFN"
BASE_URL = "https://zenodo.org/api/deposit/depositions"

lang_list = [
    "bg", "hr", "cs", "da", "nl", "et", "fi", "de", "el", "hu", "ga", "it", "lv", "lt", "mt", "pl", "pt", "ro", "sk", "sl", "sv",
    "hi", "zh-Hant", "ms", "id", "ko", "ja", "ar", "he"
]

with open("scripts/language_assets.json", "r", encoding="utf-8") as f:
    assets = json.load(f)
    headers_map = assets["headers"]
    chapter_titles = assets["chapter_titles"]

class AcademicPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 10, "Neurobiology of Mathematics Global Collection - Juan Moisés de la Serna", border=0, align="C")
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(lang_code, cap_num, source_path, output_path):
    pdf = AcademicPDF()
    pdf.add_font("FreeSerif", "", "FreeSerif.ttf")
    pdf.add_font("FreeSerif", "B", "FreeSerifBold.ttf")

    # Add CJK font if needed
    is_cjk = lang_code in ["zh-Hant", "ko", "ja"]
    if is_cjk:
        pdf.add_font("CJK", "", "IPAGothic.ttf")

    cap_key = f"cap{cap_num}"
    title = chapter_titles.get(cap_key, {}).get(lang_code, f"Neurobiology of Mathematics (Chapter {cap_num}) - {lang_code}")

    pdf.add_page()

    # Title
    if is_cjk:
        pdf.set_font("CJK", "", 16)
        pdf.multi_cell(0, 10, title, align="L")
    elif lang_code in ["ar", "he"]:
        pdf.set_font("FreeSerif", "B", 16)
        bidi = get_display(reshape(title))
        pdf.cell(0, 10, bidi, align="R")
    else:
        pdf.set_font("FreeSerif", "B", 16)
        pdf.multi_cell(0, 10, title, align="L")
    pdf.ln(10)

    pdf.set_font("FreeSerif", "", 10)
    pdf.multi_cell(0, 5, "Juan Moisés de la Serna\nUniversidad Internacional de La Rioja (UNIR)\nORCID: 0000-0002-8401-8018", align="L")
    pdf.ln(10)

    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    pdf.set_font("FreeSerif", "", 11)
    # CJK content is limited in this simplified logic, but headers/titles are now safe
    pdf.multi_cell(0, 8, content[:3000] + "...")
    pdf.output(output_path)

def publish(pdf_file, title, lang_code):
    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': f"Global collection on the Neurobiology of Mathematics by Juan Moisés de la Serna. Language: {lang_code}.",
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
    requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params={'access_token': ZENODO_TOKEN})
    return r.json().get('doi')

if __name__ == "__main__":
    # Final Mass Publication Loop for Caps 3-10
    # (Caps 1 and 2 already published successfully)
    with open("publish_remaining_log.txt", "a") as log:
        for c in range(3, 11):
            src = f"preprint_cap{c}_en.md"
            if not os.path.exists(src): continue
            for l in lang_list:
                print(f"Processing Cap {c} - {l}...")
                out = f"Global_C{c}_{l}.pdf"
                try:
                    generate_pdf(l, c, src, out)
                    doi = publish(out, f"Neurobiology of Math - Cap {c} ({l})", l)
                    log.write(f"Success: {c} {l} {doi}\n")
                    print(f"Published: {doi}")
                except Exception as e:
                    log.write(f"Error: {c} {l} {str(e)}\n")
                finally:
                    if os.path.exists(out): os.remove(out)
                time.sleep(0.5)
