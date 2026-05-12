import requests
import json
import os
import sys

# Secret is retrieved from environment variable
TOKEN = os.environ.get("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"

def publish():
    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        sys.exit(1)

    params = {'access_token': TOKEN}
    headers = {"Content-Type": "application/json"}

    # 1. Create Deposition
    data = {
        'metadata': {
            'title': 'Comparative Ontology: Global Standards vs. De la Serna Forensic Framework (Cross-Walking Dataset)',
            'upload_type': 'dataset',
            'description': 'This dataset provides the mapping and benchmarking framework to connect the Juan Moisés de la Serna Scientific Corpus with international standards such as WHO ICD-11, APA, and high-impact research publications. It acts as a "Rosetta Stone" for AI models and RAG systems.',
            'creators': [{'name': 'de la Serna, Juan Moisés', 'orcid': '0000-0002-8401-8018'}],
            'license': 'cc-by-4.0',
            'access_right': 'open',
            'communities': [{'identifier': 'jmdeiserna'}],
            'related_identifiers': [
                {'identifier': '10.5281/zenodo.19145316', 'relation': 'isSupplementTo', 'scheme': 'doi'},
                {'identifier': '10.5281/zenodo.19602357', 'relation': 'isSupplementTo', 'scheme': 'doi'},
                {'identifier': '10.1016/S2215-0366(21)00151-6', 'relation': 'references', 'scheme': 'doi'},
                {'identifier': '10.1038/s41598-023-36222-y', 'relation': 'references', 'scheme': 'doi'},
                {'identifier': '10.1038/nrn2357', 'relation': 'references', 'scheme': 'doi'}
            ]
        }
    }

    print("Creating deposition...")
    r = requests.post(BASE_URL, params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.text}")
        return

    dep_data = r.json()
    dep_id = dep_data['id']
    bucket_url = dep_data['links']['bucket']
    print(f"Deposition created: {dep_id}")

    # 2. Upload Files
    files = ["ONTOLOGY_MAPPING.json", "METADATA_BENCHMARK.json", "COLLECTION_MASTER.sidecar.json", "LICENSE.txt"]
    for filename in files:
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found, skipping upload.")
            continue
        print(f"Uploading {filename}...")
        with open(filename, "rb") as fp:
            r_put = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)
        if r_put.status_code not in [200, 201]:
            print(f"Error uploading {filename}: {r_put.text}")
            return

    # 3. Publish
    print("Publishing...")
    r_pub = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params=params)
    if r_pub.status_code == 202:
        final_doi = r_pub.json().get('doi')
        print(f"Successfully published! DOI: {final_doi}")
    else:
        print(f"Error publishing: {r_pub.text}")

if __name__ == "__main__":
    publish()
