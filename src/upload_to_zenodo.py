import requests
import os
import sys

def upload_to_zenodo(token, record_id, files_to_upload):
    """
    Uploads files to a Zenodo record by creating a new version.
    Uses the Zenodo Deposit API.
    """
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://zenodo.org/api"

    print(f"Creating new version for record {record_id}...")

    # Step 1: Create a new version draft from the latest published record
    r = requests.post(f"{base_url}/deposit/depositions/{record_id}/actions/newversion", headers=headers)
    if r.status_code != 201:
        print(f"Failed to create new version: {r.status_code}")
        print(r.text)
        sys.exit(1)

    new_version_info = r.json()
    latest_draft_url = new_version_info['links']['latest_draft']
    draft_id = latest_draft_url.split('/')[-1]
    print(f"Latest Draft ID: {draft_id}")

    # Step 2: Get the bucket URL from the draft for file uploads
    r = requests.get(latest_draft_url, headers=headers)
    draft_details = r.json()
    bucket_url = draft_details['links']['bucket']

    # Optional: Clear existing files in the draft if needed
    # (When creating a new version, files from the previous version might be present)
    for existing_file in draft_details.get('files', []):
        requests.delete(existing_file['links']['self'], headers=headers)

    # Step 3: Upload files to the bucket
    for filepath in files_to_upload:
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} not found. Skipping.")
            continue

        filename = os.path.basename(filepath)
        print(f"Uploading {filename}...")
        with open(filepath, "rb") as fp:
            r = requests.put(f"{bucket_url}/{filename}", data=fp, headers=headers)
            if r.status_code not in [200, 201]:
                print(f"Failed to upload {filename}: {r.status_code}")
                print(r.text)
                sys.exit(1)
            print(f"Uploaded {filename} successfully.")

    # Step 4: Update metadata if necessary (e.g. set publication date)
    # The new version needs a publication date to be published
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    metadata = draft_details['metadata']
    metadata['publication_date'] = today

    r = requests.put(latest_draft_url, json={"metadata": metadata}, headers=headers)
    if r.status_code != 200:
        print(f"Failed to update metadata: {r.status_code}")
        print(r.text)

    # Step 5: Publish the draft
    publish_url = draft_details['links']['publish']
    print("Publishing new version...")
    r = requests.post(publish_url, headers=headers)
    if r.status_code != 202:
        print(f"Failed to publish: {r.status_code}")
        print(r.text)
        sys.exit(1)

    published_data = r.json()
    print(f"Published successfully! New DOI: {published_data.get('doi')}")
    print(f"Record URL: {published_data['links']['record_html']}")

if __name__ == "__main__":
    TOKEN = os.getenv("ZENODO_TOKEN")
    # RECORD_ID should be the 'recid' or 'id' of the record to update
    RECORD_ID = os.getenv("ZENODO_RECORD_ID", "19145316")
    FILES = ["COMMERCIAL_LICENSE.md", "COMMERCIAL_LICENSE.pdf"]

    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        sys.exit(1)

    upload_to_zenodo(TOKEN, RECORD_ID, FILES)
