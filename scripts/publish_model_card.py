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
            'title': 'Juan de la Serna Corpus Model Card & AI Governance Framework',
            'upload_type': 'dataset',
            'description': 'This record contains the Model Card and AI Governance Framework for the Juan Moisés de la Serna Scientific Corpus, designed for ethical AI training and deployment.',
            'creators': [{'name': 'de la Serna, Juan Moisés', 'orcid': '0000-0002-8401-8018'}],
            'license': 'cc-by-4.0',
            'access_right': 'open',
            'communities': [{'identifier': 'jmdeiserna'}]
        }
    }

    print("Creating deposition...")
    r = requests.post(BASE_URL, params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.text}")
        return

    dep_data = r.json()
    dep_id = dep_data['id']
    doi = dep_data.get('metadata', {}).get('prereserve_doi', {}).get('doi')
    bucket_url = dep_data['links']['bucket']
    print(f"Deposition created: {dep_id}, Reserved DOI: {doi}")

    # 2. Update placeholders in files locally with the DOI
    # Note: This modifies the files in place for upload
    files_to_update = ["MODEL_CARD.md", "schema.jsonld"]
    for filename in files_to_update:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read()

            # Replace common DOI placeholders
            updated_content = content.replace("[TU_DOI]", doi).replace("[TU_ID]", str(dep_id)).replace("10.5281/zenodo.19145316", doi)

            with open(filename, "w") as f:
                f.write(updated_content)
            print(f"Updated {filename} with DOI {doi}.")

    # 3. Upload Files
    files = ["MODEL_CARD.md", "LICENSE.txt", "schema.jsonld", "SEO_OPTIMIZED_METADATA.json"]
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

    # 4. Publish
    print("Publishing...")
    r_pub = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params=params)
    if r_pub.status_code == 202:
        final_doi = r_pub.json().get('doi')
        print(f"Successfully published! DOI: {final_doi}")
    else:
        print(f"Error publishing: {r_pub.text}")

if __name__ == "__main__":
    publish()
