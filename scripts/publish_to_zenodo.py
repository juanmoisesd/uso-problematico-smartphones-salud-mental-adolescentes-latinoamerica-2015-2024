import os
import requests
import glob
import time

def publish_to_zenodo(filepath, token):
    print(f"Publishing {filepath} to Zenodo...")
    filename = os.path.basename(filepath)
    topic = filename.replace("Preprint_Neuro_", "").replace("_JuanMoisesdelaSerna.pdf", "").replace("_", " ")

    headers = {"Content-Type": "application/json"}
    params = {'access_token': token}

    # 1. Create deposition
    r = requests.post('https://zenodo.org/api/deposit/depositions',
                      params=params,
                      json={},
                      headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.status_code} - {r.json()}")
        return None

    res = r.json()
    deposition_id = res['id']
    # bucket_url might not be in the response in some API versions, or might be elsewhere
    # In newer Zenodo API, it's in links['bucket']
    bucket_url = res['links']['bucket']

    # 2. Upload file
    with open(filepath, "rb") as fp:
        # Construct the upload URL correctly
        upload_url = f"{bucket_url}/{filename}"
        r = requests.put(upload_url,
                         data=fp,
                         params=params)

    # The error showed r.json() returning the file object, which means status was likely 201 or 200
    if r.status_code not in [200, 201]:
        print(f"Error uploading file: {r.status_code} - {r.json()}")
        return None

    print(f"File uploaded successfully to {deposition_id}")

    # 3. Add metadata
    data = {
        'metadata': {
            'title': f'Preprint: Neurociencia de las Matematicas - {topic}',
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': f'Manuscrito cientifico sobre {topic} en el contexto de la neurociencia de las matematicas.',
            'creators': [{'name': 'de la Serna, Juan Moises', 'affiliation': 'Universidad Internacional de La Rioja (UNIR)', 'orcid': '0000-0002-8401-8018'}],
            'license': 'cc-by-4.0',
            'access_right': 'open'
        }
    }
    r = requests.put(f'https://zenodo.org/api/deposit/depositions/{deposition_id}',
                     params=params,
                     json=data,
                     headers=headers)
    if r.status_code != 200:
        print(f"Error adding metadata: {r.status_code} - {r.json()}")
        return None

    # 4. Publish
    r = requests.post(f'https://zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish',
                      params=params)
    if r.status_code != 202:
        print(f"Error publishing: {r.status_code} - {r.json()}")
        return None

    doi = r.json().get('doi', 'Pending')
    print(f"Published successfully! DOI: {doi}")
    return doi

if __name__ == "__main__":
    token = os.getenv("ZENODO_TOKEN")
    if not token:
        print("ZENODO_TOKEN environment variable not set.")
    else:
        pdfs = glob.glob("preprints/pdfs/*.pdf")
        for pdf in sorted(pdfs):
            publish_to_zenodo(pdf, token)
            time.sleep(2) # Increased sleep
