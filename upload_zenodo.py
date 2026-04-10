import requests
import json
import os
import re

ZENODO_TOKEN = os.getenv("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api"

def upload_to_zenodo(pdf_path, md_path):
    if not ZENODO_TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return None

    # 1. Create a new deposition
    headers = {"Content-Type": "application/json"}
    params = {'access_token': ZENODO_TOKEN}

    r = requests.post(f"{BASE_URL}/deposit/depositions", params=params, json={}, headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.json()}")
        return None

    deposition_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']

    # 2. Upload the file
    filename = os.path.basename(pdf_path)
    with open(pdf_path, "rb") as f:
        r = requests.put(f"{bucket_url}/{filename}", data=f, params=params)

    if r.status_code != 201:
        print(f"Error uploading file: {r.json()}")
        return None

    # 3. Add metadata
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    title_match = re.search(r"^\*\*Título:\*\* (.*)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else filename

    abstract_match = re.search(r"### Abstract\n(.*?)\n\n\*\*Keywords:\*\*", content, re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ""

    keywords_match = re.search(r"\*\*Keywords:\*\* (.*)$", content, re.MULTILINE)
    keywords = [k.strip() for k in keywords_match.group(1).split(",")] if keywords_match else []

    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': abstract,
            'creators': [{'name': 'de la Serna, Juan Moisés',
                          'affiliation': 'Universidad Internacional de La Rioja (UNIR)',
                          'orcid': '0000-0002-8401-8018'}],
            'keywords': keywords,
            'access_right': 'open',
            'license': 'cc-by-4.0',
            'communities': [{'identifier': 'psychology'}, {'identifier': 'neuroscience'}]
        }
    }

    r = requests.put(f"{BASE_URL}/deposit/depositions/{deposition_id}", params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        print(f"Error adding metadata for {filename}: {r.json()}")
        # Check if communities exist, if not, try without communities
        if "communities" in str(r.json()):
             print("Retrying without communities...")
             del data['metadata']['communities']
             r = requests.put(f"{BASE_URL}/deposit/depositions/{deposition_id}", params=params, data=json.dumps(data), headers=headers)
             if r.status_code != 200:
                 print(f"Error adding metadata (retry) for {filename}: {r.json()}")
                 return None
        else:
             return None

    # 4. Publish
    r = requests.post(f"{BASE_URL}/deposit/depositions/{deposition_id}/actions/publish", params=params)
    if r.status_code != 202:
        print(f"Error publishing {filename}: {r.json()}")
        return None

    doi = r.json()['doi']
    record_url = r.json()['links']['record_html']
    print(f"Successfully published: {filename} -> DOI: {doi}")
    return {"filename": filename, "doi": doi, "url": record_url}

if __name__ == "__main__":
    mappings = [
        ("Preprint_Crisis_Replicabilidad_JuanMoisésdelaSerna.pdf", "preprint_01_crisis_replicabilidad.md"),
        ("Preprint_Validez_DSM_JuanMoisésdelaSerna.pdf", "preprint_02_validez_dsm.md"),
        ("Preprint_Psicofarmacos_Psicoterapia_JuanMoisésdelaSerna.pdf", "preprint_03_psicofarmacos_psicoterapia.md"),
        ("Preprint_Neurodeterminismo_JuanMoisésdelaSerna.pdf", "preprint_04_neurodeterminismo.md"),
        ("Preprint_Terapias_Alternativas_JuanMoisésdelaSerna.pdf", "preprint_05_terapias_alternativas.md"),
        ("Preprint_Inteligencia_Genetica_JuanMoisésdelaSerna.pdf", "preprint_06_inteligencia_genetica.md"),
        ("Preprint_Sesgos_WEIRD_JuanMoisésdelaSerna.pdf", "preprint_07_sesgos_weird.md"),
        ("Preprint_Psicologia_Positiva_JuanMoisésdelaSerna.pdf", "preprint_08_psicologia_positiva.md"),
        ("Preprint_IA_Salud_Mental_JuanMoisésdelaSerna.pdf", "preprint_09_ia_salud_mental.md"),
        ("Preprint_Etica_Experimentacion_JuanMoisésdelaSerna.pdf", "preprint_10_etica_experimentacion.md"),
    ]

    results = []
    for pdf, md in mappings:
        print(f"Uploading {pdf}...")
        res = upload_to_zenodo(f"preprints/{pdf}", f"preprints/{md}")
        if res:
            results.append(res)

    with open("zenodo_results.json", "w") as f:
        json.dump(results, f, indent=4)
