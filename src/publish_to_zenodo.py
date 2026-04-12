import os
import requests
import json

def publish_preprint(md_path, pdf_path, token, lang="es"):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Extract title from Markdown
    with open(md_path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip("# ")

    data = {
        "metadata": {
            "title": first_line,
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": f"Scientific Meta-Analysis: {first_line}" if lang == "en" else f"Meta-análisis científico: {first_line}",
            "creators": [{"name": "de la Serna, Juan Moisés", "affiliation": "Universidad Internacional de La Rioja (UNIR)", "orcid": "0000-0002-8401-8018"}],
            "access_right": "open",
            "license": "cc-by-4.0",
            "language": lang
        }
    }

    # Create deposition
    r = requests.post("https://zenodo.org/api/deposit/depositions", headers=headers, data=json.dumps(data))
    if r.status_code != 201:
        print(f"Error creating deposition for {md_path}: {r.json()}")
        return None

    deposition_id = r.json()["id"]
    bucket_url = r.json()["links"]["bucket"]

    # Upload PDF
    filename = os.path.basename(pdf_path)
    upload_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"}
    with open(pdf_path, "rb") as f:
        r = requests.put(f"{bucket_url}/{filename}", headers=upload_headers, data=f)

    if r.status_code != 201:
        print(f"Error uploading file for {md_path}: {r.json()}")
        return None

    # Publish
    r = requests.post(f"https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish", headers=headers)
    if r.status_code != 202:
        print(f"Error publishing {md_path}: {r.json()}")
        return None

    return r.json()["doi"]

def process_dir(lang, token):
    preprints_dir = f"preprints/{lang}"
    if not os.path.exists(preprints_dir):
        return

    md_files = [f for f in os.listdir(preprints_dir) if f.endswith(".md")]
    for md_file in md_files:
        md_path = os.path.join(preprints_dir, md_file)
        # Use a more robust way to match PDF
        topic = md_file.replace("Chapter_", "").replace(".md", "")
        topic_clean = topic.split("_", 1)[1] if "_" in topic else topic
        pdf_file = f"Preprint_Neuro_{topic_clean}_JuanMoisésdelaSerna.pdf"
        pdf_path = os.path.join(preprints_dir, pdf_file)

        if os.path.exists(pdf_path):
            print(f"Publishing {md_file} [{lang}] to Zenodo...")
            doi = publish_preprint(md_path, pdf_path, token, lang=lang)
            if doi:
                print(f"Published: {doi}")

def main():
    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        print("ZENODO_TOKEN environment variable not set.")
        return

    # Assuming ES was already published, but script can handle both.
    # To avoid duplicates if main() is called repeatedly, we might want logic to check.
    # For this task, we focus on publishing 'en'.
    process_dir("en", token)

if __name__ == "__main__":
    main()
