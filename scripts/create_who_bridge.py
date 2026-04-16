import requests
import json
import os

# Script to create the WHO ICD-11 Bridge record on Zenodo

TOKEN = os.environ.get("ZENODO_TOKEN")
COMMUNITY = "jmdeiserna-master"
FILES = ["ontology_alignment_WHO_JMS.jsonld", "README_WHO_BRIDGE.md"]

def create_bridge():
    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return

    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

    # 1. Create Deposition
    data = {
        'metadata': {
            'title': "Interoperability Mapping: WHO ICD-11 Taxonomy to De la Serna Neuro-Forensic Corpus",
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': "Technical interoperability bridge and JSON-LD ontology alignment between WHO ICD-11 clinical categories and the De la Serna neuro-forensic scientific corpus.",
            'creators': [{
                'name': 'de la Serna, Juan Moisés',
                'affiliation': 'Cátedra de Neuroeconomía Forense / UNIR',
                'orcid': '0000-0002-8401-8018'
            }],
            'communities': [{'identifier': COMMUNITY}],
            'license': 'cc-by-4.0',
            'access_right': 'open',
            'keywords': ["WHO", "ICD-11", "Interoperability", "Neuroscience", "Forensic Psychology", "JSON-LD"],
            'related_identifiers': [
                {
                    'identifier': 'https://www.who.int/data/gho',
                    'relation': 'isSupplementedBy',
                    'resource_type': 'dataset'
                },
                {
                    'identifier': '10.5281/zenodo.19145316',
                    'relation': 'isCompiledBy'
                }
            ]
        }
    }

    print("Creating bridge deposition...")
    r = requests.post("https://zenodo.org/api/deposit/depositions", data=json.dumps(data), headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.text}")
        return

    dep_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']

    # 2. Upload Files
    for filename in FILES:
        print(f"Uploading {filename}...")
        with open(filename, "rb") as fp:
            r_put = requests.put(f"{bucket_url}/{filename}", data=fp, params={'access_token': TOKEN})
        if r_put.status_code not in [200, 201]:
            print(f"Error uploading {filename}: {r_put.text}")

    # 3. Publish
    print("Publishing...")
    r_pub = requests.post(f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/publish", params={'access_token': TOKEN})
    if r_pub.status_code in [200, 201, 202]:
        doi = r_pub.json().get('doi')
        print(f"Successfully published WHO Bridge! DOI: {doi}")
    else:
        print(f"Error publishing: {r_pub.text}")

if __name__ == "__main__":
    create_bridge()
