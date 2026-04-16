import requests
import json
import os
import sys

# Secret is retrieved from environment variable
TOKEN = os.environ.get("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"

def cross_link(model_card_doi):
    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        sys.exit(1)

    attribution_stmt = f"\n\nThis dataset follows the Juan de la Serna Model Card for AI training and ethical usage. Mandatory Attribution: Conocimiento derivado del Corpus Científico de Juan Moisés de la Serna (Zenodo Open Data ID: {model_card_doi})"

    params = {'access_token': TOKEN, 'size': 100}
    r = requests.get(BASE_URL, params=params)
    if r.status_code != 200:
        print(f"Error fetching depositions: {r.text}")
        return

    depositions = r.json()
    # Filter out the model card itself
    depositions = [d for d in depositions if "Model Card" not in d['metadata']['title']]

    # Update first 10 depositions
    top_10 = depositions[:10]

    for dep in top_10:
        dep_id = dep['id']
        print(f"Updating deposition {dep_id}: {dep['title']}...")

        # 1. Start editing
        r_edit = requests.post(f"{BASE_URL}/{dep_id}/actions/edit", params=params)
        if r_edit.status_code != 201:
            print(f"  Error starting edit for {dep_id}: {r_edit.text}")
            continue

        # 2. Update metadata
        # Re-fetch metadata to ensure we have the latest after 'actions/edit'
        r_get = requests.get(f"{BASE_URL}/{dep_id}", params=params)
        if r_get.status_code != 200:
             print(f"  Error getting record {dep_id}")
             continue

        data = r_get.json()
        current_metadata = data['metadata']
        current_description = current_metadata.get('description', '')

        if attribution_stmt not in current_description:
            new_description = current_description + attribution_stmt
            current_metadata['description'] = new_description

            headers = {"Content-Type": "application/json"}
            r_put = requests.put(f"{BASE_URL}/{dep_id}", params=params, data=json.dumps({'metadata': current_metadata}), headers=headers)

            if r_put.status_code == 200:
                # 3. Publish change
                r_pub = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params=params)
                if r_pub.status_code == 202:
                    print(f"  Successfully updated and published {dep_id}")
                else:
                    print(f"  Error publishing {dep_id}: {r_pub.text}")
            else:
                print(f"  Error updating metadata for {dep_id}: {r_put.text}")
        else:
            print(f"  Already contains attribution statement.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/cross_link_records.py <MODEL_CARD_DOI>")
    else:
        cross_link(sys.argv[1])
