import sys
import os
import json
import time

sys.path.append(os.getcwd())
from publish_multi_lang import generate_pdf, publish_to_zenodo

# List of 29 target languages
lang_list = [
    "bg", "hr", "cs", "da", "nl", "et", "fi", "de", "el", "hu", "ga", "it", "lv", "lt", "mt", "pl", "pt", "ro", "sk", "sl", "sv",
    "hi", "zh-Hant", "ms", "id", "ko", "ja", "ar", "he"
]

with open("scripts/language_assets.json", "r", encoding="utf-8") as f:
    assets = json.load(f)
    chapter_titles = assets["chapter_titles"]

def run_publication():
    log_file = "publish_log.txt"
    with open(log_file, "a", encoding="utf-8") as log:
        # 1. Publish Global Collection (10 chapters x 29 languages)
        for cap_num in range(1, 11):
            source_en = f"preprint_cap{cap_num}_en.md"
            if not os.path.exists(source_en):
                continue

            for lang in lang_list:
                print(f"Processing Cap {cap_num} - {lang}...")
                pdf_path = f"Preprint_Neuro_Cap{cap_num}_{lang}.pdf"
                try:
                    generate_pdf(lang, cap_num, source_en, pdf_path)
                    title = chapter_titles.get(f"cap{cap_num}", {}).get(lang, f"Neurobiology of Mathematics (Chapter {cap_num}) - {lang}")
                    doi = publish_to_zenodo(pdf_path, title, lang)
                    if doi:
                        log.write(f"Success: {cap_num} {lang} {doi}\n")
                        print(f"Published: {doi}")
                    else:
                        log.write(f"Failed: {cap_num} {lang}\n")
                except Exception as e:
                    log.write(f"Error: {cap_num} {lang} {str(e)}\n")
                finally:
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                time.sleep(1) # Be nice to the API

if __name__ == "__main__":
    run_publication()
