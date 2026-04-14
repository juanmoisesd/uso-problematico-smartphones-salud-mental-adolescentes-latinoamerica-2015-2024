import sys
import os
import json
import time
import requests
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Configuration
ZENODO_TOKEN = os.environ.get("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"

# List of 29 target languages for the Global Collection
global_langs = [
    "bg", "hr", "cs", "da", "nl", "et", "fi", "de", "el", "hu", "ga", "it", "lv", "lt", "mt", "pl", "pt", "ro", "sk", "sl", "sv",
    "hi", "zh-Hant", "ms", "id", "ko", "ja", "ar", "he"
]

# Load shared assets
with open("scripts/language_assets.json", "r", encoding="utf-8") as f:
    assets = json.load(f)
    headers_map = assets["headers"]
    chapter_titles = assets["chapter_titles"]

class AcademicPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 10, "Neurobiology of Mathematics - Juan Moisés de la Serna", border=0, align="C")
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_and_publish(lang_code, cap_num, source_path, is_brief=False):
    # 1. Generate PDF
    pdf = AcademicPDF()
    pdf.add_font("FreeSerif", "", "FreeSerif.ttf")
    pdf.add_font("FreeSerif", "B", "FreeSerifBold.ttf")
    if lang_code in ["zh-Hant", "ko", "ja"]:
        pdf.add_font("CJK", "", "IPAGothic.ttf")
        pdf.set_font("CJK", "", 16)
    else:
        pdf.set_font("FreeSerif", "B", 16)

    cap_key = f"cap{cap_num}"
    title = chapter_titles.get(cap_key, {}).get(lang_code, f"Neurobiology of Mathematics (Cap {cap_num}) - {lang_code}")
    if is_brief: title = f"Policy Brief: {title}"

    pdf.add_page()

    # Render Title
    if lang_code in ["ar", "he"]:
        bidi = get_display(reshape(title))
        pdf.cell(0, 10, bidi, ln=1, align="R")
    else:
        pdf.multi_cell(0, 10, title, align="L")
    pdf.ln(10)

    # Author
    pdf.set_font("FreeSerif", "", 10)
    pdf.multi_cell(0, 5, "Juan Moisés de la Serna\nUniversidad Internacional de La Rioja (UNIR)\nORCID: 0000-0002-8401-8018", align="L")
    pdf.ln(10)

    # Content (Preview/Partial for mass collection, Full for main)
    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    pdf.set_font("FreeSerif", "", 11)
    limit = 8000 if not is_brief and lang_code in ["en", "es"] else 3000
    pdf.multi_cell(0, 8, content[:limit].replace("#", "").replace("**", "") + "...")

    pdf_name = f"Output_{lang_code}_{cap_num}.pdf"
    pdf.output(pdf_name)

    # 2. Publish to Zenodo
    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': f"Research document on the neurobiology of mathematics. Chapter: {cap_num}. Language: {lang_code}. Author: Juan Moisés de la Serna.",
            'creators': [{'name': 'de la Serna, Juan Moisés', 'affiliation': 'Universidad Internacional de La Rioja (UNIR)', 'orcid': '0000-0002-8401-8018'}],
            'license': 'cc-by-4.0',
            'language': lang_code,
            'access_right': 'open'
        }
    }

    doi = None
    try:
        r = requests.post(BASE_URL, params={'access_token': ZENODO_TOKEN}, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if r.status_code == 201:
            dep_id = r.json()['id']
            bucket_url = r.json()['links']['bucket']
            with open(pdf_name, "rb") as fp:
                requests.put(f"{bucket_url}/{os.path.basename(pdf_name)}", data=fp, params={'access_token': ZENODO_TOKEN})
            r_pub = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params={'access_token': ZENODO_TOKEN})
            if r_pub.status_code == 202:
                doi = r_pub.json().get('doi')
    except Exception as e:
        print(f"Error publishing {lang_code} {cap_num}: {e}")

    if os.path.exists(pdf_name): os.remove(pdf_name)
    return doi

if __name__ == "__main__":
    master_log = "master_publish_log.txt"
    with open(master_log, "a") as log:
        # Phase 1: Spanish Policy Briefs (1-10)
        print("Publishing Spanish Policy Briefs...")
        for i in range(1, 11):
            doi = generate_and_publish("es", i, f"brief_cap{i}.md", is_brief=True)
            log.write(f"ES {i} {doi}\n")
            print(f"ES {i} -> {doi}")
            time.sleep(1)

        # Phase 2: English Preprints (1-10)
        print("Publishing English Preprints...")
        for i in range(1, 11):
            doi = generate_and_publish("en", i, f"preprint_cap{i}_en.md")
            log.write(f"EN {i} {doi}\n")
            print(f"EN {i} -> {doi}")
            time.sleep(1)

        # Phase 3: Global Collection (290)
        print("Publishing Global Collection...")
        for i in range(1, 11):
            for lang in global_langs:
                doi = generate_and_publish(lang, i, f"preprint_cap{i}_en.md")
                log.write(f"GLOBAL {lang} {i} {doi}\n")
                print(f"GLOBAL {lang} {i} -> {doi}")
                time.sleep(0.5)
