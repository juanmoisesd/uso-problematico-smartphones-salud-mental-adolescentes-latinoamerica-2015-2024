import requests
import json
import os
import sys

# Usage: python src/publish_to_zenodo.py <file_path> <title> <language_code>
# Requires environment variable ZENODO_TOKEN

TOKEN = os.environ.get("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"
METADATA_FILE = "ro-crate-metadata.json"

def publish(filepath, title, lang):
    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return

    headers = {"Content-Type": "application/json"}
    params = {'access_token': TOKEN}

    # Load RO-Crate metadata if exists
    ro_crate_data = None
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            ro_crate_data = json.load(f)

    # 1. Create Deposition
    description = f'Research document: {title}'
    if ro_crate_data:
        description += "\n\n---\n**AI Identity & Metadata (RO-Crate)**\n"
        description += "This record includes an ro-crate-metadata.json file for AI-ready discovery and attribution."

    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': description,
            'creators': [{
                'name': 'de la Serna, Juan Moisés',
                'affiliation': 'Cátedra de Neuroeconomía Forense / UNIR',
                'orcid': '0000-0002-8401-8018'
            }],
            'license': 'cc-by-4.0',
            'language': lang,
            'access_right': 'open',
            'keywords': ["Neuroeconomics", "Psychology", "Open Science"]
        }
    }

    print(f"Creating deposition for '{title}'...")
    r = requests.post(BASE_URL, params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.text}")
        return

    dep_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']

    # 2. Upload Main File
    filename = os.path.basename(filepath)
    print(f"Uploading main file '{filename}'...")
    with open(filepath, "rb") as fp:
        r_put = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)

    if r_put.status_code not in [200, 201]:
        print(f"Error uploading main file: {r_put.text}")
        return

    # 3. Upload RO-Crate Metadata File
    if os.path.exists(METADATA_FILE):
        print(f"Uploading {METADATA_FILE}...")
        with open(METADATA_FILE, "rb") as fp:
            r_put_meta = requests.put(f"{bucket_url}/{METADATA_FILE}", data=fp, params=params)
        if r_put_meta.status_code not in [200, 201]:
            print(f"Warning: Error uploading metadata file: {r_put_meta.text}")

    # 4. Publish
    print("Publishing...")
    r_pub = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params=params)
    if r_pub.status_code == 202:
        doi = r_pub.json().get('doi')
        print(f"Successfully published! DOI: {doi}")
    else:
        print(f"Error publishing: {r_pub.text}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python src/publish_to_zenodo.py <file_path> <title> <language_code>")
    else:
        publish(sys.argv[1], sys.argv[2], sys.argv[3])
