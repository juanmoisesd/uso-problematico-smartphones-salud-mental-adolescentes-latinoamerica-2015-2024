import requests
import os
import sys
import csv

def tag_records(token, record_ids, tag):
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://zenodo.org/api"

    for rid in record_ids:
        print(f"Tagging record {rid} with {tag}...")

        # In Zenodo, to update a published record, we usually need to:
        # 1. Create a new version OR
        # 2. If metadata update is allowed on published records (sometimes it is via deposit API)

        # Let's try to edit the metadata of the current record via Deposit API
        # First we need to get into "edit" mode if it's published
        edit_url = f"{base_url}/deposit/depositions/{rid}/actions/edit"
        r = requests.post(edit_url, headers=headers)

        if r.status_code not in [201, 200]:
            print(f"Could not open record {rid} for editing: {r.status_code}")
            continue

        # Get current metadata
        r = requests.get(f"{base_url}/deposit/depositions/{rid}", headers=headers)
        dep = r.json()
        metadata = dep['metadata']

        # Add tag to keywords
        keywords = metadata.get('keywords', [])
        if tag not in keywords:
            keywords.append(tag)
            metadata['keywords'] = keywords

            # Update metadata
            r = requests.put(f"{base_url}/deposit/depositions/{rid}", json={"metadata": metadata}, headers=headers)
            if r.status_code == 200:
                # Publish changes
                requests.post(f"{base_url}/deposit/depositions/{rid}/actions/publish", headers=headers)
                print(f"Successfully tagged {rid}")
            else:
                print(f"Failed to update metadata for {rid}: {r.status_code}")
        else:
            print(f"Tag already present in {rid}")
            # Discard edit
            requests.post(f"{base_url}/deposit/depositions/{rid}/actions/discard", headers=headers)

if __name__ == "__main__":
    TOKEN = os.getenv("ZENODO_TOKEN")
    TAG = "Migracion-Salud-Mental-JMS"

    # Identifying record IDs from relevant_records.csv
    # The format is "title","doi","url",...
    rids = []
    if os.path.exists("relevant_records.csv"):
        with open("relevant_records.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    doi = row[1]
                    rid = doi.split('.')[-1]
                    rids.append(rid)

    if not TOKEN:
        print("Error: ZENODO_TOKEN not set.")
        sys.exit(1)

    if rids:
        tag_records(TOKEN, rids, TAG)
    else:
        print("No relevant records found to tag.")
