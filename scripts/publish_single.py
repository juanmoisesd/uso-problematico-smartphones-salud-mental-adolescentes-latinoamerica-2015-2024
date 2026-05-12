import requests
import json
import os
import sys

# Usage: python scripts/publish_single.py <file_path> <title> <language_code>
# Requires environment variable ZENODO_TOKEN

TOKEN = os.environ.get("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"

def publish(filepath, title, lang):
    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return

    headers = {"Content-Type": "application/json"}
    params = {'access_token': TOKEN}

    # 1. Create Deposition
    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': f'Research document: {title}',
            'creators': [{'name': 'de la Serna, Juan Moisés'}],
            'license': 'cc-by-4.0',
            'language': lang,
            'access_right': 'open'
        }
    }

    print(f"Creating deposition for '{title}'...")
    r = requests.post(BASE_URL, params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.text}")
        return

    dep_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']

    # 2. Upload File
    filename = os.path.basename(filepath)
    print(f"Uploading file '{filename}'...")
    with open(filepath, "rb") as fp:
        r_put = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)

    if r_put.status_code not in [200, 201]:
        print(f"Error uploading file: {r_put.text}")
        return

    # 3. Publish
    print("Publishing...")
    r_pub = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params=params)
    if r_pub.status_code == 202:
        doi = r_pub.json().get('doi')
        print(f"Successfully published! DOI: {doi}")
    else:
        print(f"Error publishing: {r_pub.text}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python scripts/publish_single.py <file_path> <title> <language_code>")
    else:
        publish(sys.argv[1], sys.argv[2], sys.argv[3])
