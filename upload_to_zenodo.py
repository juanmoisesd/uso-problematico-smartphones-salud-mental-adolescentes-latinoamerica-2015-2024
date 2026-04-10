import requests
import json
import os
import time

# Get token from environment variable
ACCESS_TOKEN = os.getenv('ZENODO_TOKEN')
BASE_URL = 'https://zenodo.org/api/deposit/depositions'

def upload_to_zenodo(topic, pdf_path):
    if not ACCESS_TOKEN:
        print("ZENODO_TOKEN not set. Skipping upload.")
        return None

    print(f"Uploading {topic['title']}...")

    headers = {"Content-Type": "application/json"}
    params = {'access_token': ACCESS_TOKEN}

    metadata = {
        'metadata': {
            'title': topic['title'],
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': topic['abstract'],
            'creators': [{'name': 'de la Serna, Juan Moises', 'affiliation': 'UNIR', 'orcid': '0000-0002-8401-8018'}],
            'keywords': topic['keywords'],
            'license': 'cc-by-4.0',
            'access_right': 'open',
            'communities': [{'identifier': 'neuroscience'}]
        }
    }

    # 1. Create deposition
    r = requests.post(BASE_URL, params=params, json=metadata, headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.json()}")
        return None

    deposition_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']

    # 2. Upload file
    filename = os.path.basename(pdf_path)
    with open(pdf_path, "rb") as fp:
        r = requests.put(
            f"{bucket_url}/{filename}",
            data=fp,
            params=params,
        )

    if r.status_code not in [200, 201]:
        print(f"Error uploading file: {r.json()}")
        return None

    # 3. Publish
    publish_url = f"{BASE_URL}/{deposition_id}/actions/publish"
    r = requests.post(publish_url, params=params)

    if r.status_code != 202:
        print(f"Error publishing: {r.json()}")
        r_get = requests.get(f"{BASE_URL}/{deposition_id}", params=params)
        data = r_get.json()
        return {
            'title': topic['title'],
            'doi': data.get('metadata', {}).get('prereserve_doi', {}).get('doi', 'Pending'),
            'url': f"https://zenodo.org/record/{deposition_id}"
        }

    res = r.json()
    return {
        'title': topic['title'],
        'doi': res['doi'],
        'url': res['links']['html']
    }

if __name__ == "__main__":
    with open('metadata/preprints_metadata.json', 'r') as f:
        topics = json.load(f)

    results = []
    for topic in topics:
        pdf_filename = f"preprints/Preprint_Neuro_{topic['id']}_JuanMoisesdelaSerna.pdf"
        if os.path.exists(pdf_filename):
            res = upload_to_zenodo(topic, pdf_filename)
            if res:
                results.append(res)
            time.sleep(2)

    with open('metadata/zenodo_results.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("Zenodo process complete.")
