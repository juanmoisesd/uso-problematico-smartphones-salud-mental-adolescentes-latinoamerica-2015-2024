import requests
import json
import os

ZENODO_TOKEN = os.getenv("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"

def publish_to_zenodo(pdf_file, title, abstract, lang_code):
    if not ZENODO_TOKEN:
        print("ZENODO_TOKEN not set")
        return None
    headers = {"Content-Type": "application/json"}
    params = {'access_token': ZENODO_TOKEN}
    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': f"<p>{abstract}</p>",
            'creators': [{'name': 'de la Serna, Juan Moisés', 'affiliation': 'Universidad Internacional de La Rioja (UNIR)', 'orcid': '0000-0002-8401-8018'}],
            'license': 'cc-by-4.0',
            'language': lang_code,
            'access_right': 'open'
        }
    }
    r = requests.post(BASE_URL, params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 201:
        return None
    dep_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']
    filename = os.path.basename(pdf_file)
    with open(pdf_file, "rb") as fp:
        r = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)
    if r.status_code not in [200, 201]:
        requests.post(f"{BASE_URL}/{dep_id}/files", params=params, files={'file': open(pdf_file, 'rb')})
    r = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params=params)
    if r.status_code == 202:
        return r.json().get('doi')
    return None
