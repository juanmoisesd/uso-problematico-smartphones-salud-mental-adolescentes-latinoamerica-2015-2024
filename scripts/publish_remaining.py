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

# List of 29 target languages
global_langs = [
    "bg", "hr", "cs", "da", "nl", "et", "fi", "de", "el", "hu", "ga", "it", "lv", "lt", "mt", "pl", "pt", "ro", "sk", "sl", "sv",
    "hi", "zh-Hant", "ms", "id", "ko", "ja", "ar", "he"
]

# Load shared assets
with open("scripts/language_assets.json", "r", encoding="utf-8") as f:
    assets = json.load(f)
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

def generate_and_publish(lang_code, cap_num, source_path):
    pdf = AcademicPDF()
    pdf.add_font("FreeSerif", "", "FreeSerif.ttf")
    pdf.add_font("FreeSerif", "B", "FreeSerifBold.ttf")

    # Use IPAGothic for CJK (it has better support for Chinese/Japanese/Korean)
    if lang_code in ["zh-Hant", "ko", "ja"]:
        pdf.add_font("CJK", "", "IPAGothic.ttf")
        pdf.set_font("CJK", "", 16)
    else:
        pdf.set_font("FreeSerif", "B", 16)

    cap_key = f"cap{cap_num}"
    title = chapter_titles.get(cap_key, {}).get(lang_code, f"Neurobiology of Mathematics (Cap {cap_num}) - {lang_code}")

    pdf.add_page()

    # Render Title
    if lang_code in ["ar", "he"]:
        bidi = get_display(reshape(title))
        pdf.cell(0, 10, bidi, align="R")
    else:
        pdf.multi_cell(0, 10, title, align="L")
    pdf.ln(10)

    pdf.set_font("FreeSerif", "", 10)
    pdf.multi_cell(0, 5, "Juan Moisés de la Serna\nUniversidad Internacional de La Rioja (UNIR)\nORCID: 0000-0002-8401-8018", align="L")
    pdf.ln(10)

    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    pdf.set_font("FreeSerif", "", 11)
    pdf.multi_cell(0, 8, content[:3000] + "...")

    pdf_name = f"Global_{lang_code}_{cap_num}.pdf"
    pdf.output(pdf_name)

    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': f"Global collection on the neurobiology of mathematics. Chapter {cap_num}. Language: {lang_code}. Author: Juan Moisés de la Serna.",
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
    except Exception:
        pass

    if os.path.exists(pdf_name): os.remove(pdf_name)
    return doi

if __name__ == "__main__":
    # Publish Chapters 3 to 10 for all 29 languages
    # Plus the missing zh-Hant for Caps 1 and 2
    with open("publish_final_run.txt", "a") as log:
        # Fix missing zh-Hant for 1 and 2
        for c in [1, 2]:
            doi = generate_and_publish("zh-Hant", c, f"preprint_cap{c}_en.md")
            log.write(f"FIX zh-Hant {c} {doi}\n")
            print(f"FIX zh-Hant {c} -> {doi}")

        for c in range(3, 11):
            src = f"preprint_cap{c}_en.md"
            if not os.path.exists(src): continue
            for l in global_langs:
                doi = generate_and_publish(l, c, src)
                log.write(f"GLOBAL {l} {c} {doi}\n")
                print(f"GLOBAL {l} {c} -> {doi}")
                time.sleep(0.3)
