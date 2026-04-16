import requests
import json
import os

# Updated seed script for Zenodo API v1/v2 hybrid behavior

TOKEN = os.environ.get("ZENODO_TOKEN")
RECORD_ID = "19145316"
METADATA_FILE = "ro-crate-metadata.json"

def seed():
    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}

    # 1. Action: Edit
    print(f"Opening deposition {RECORD_ID} for editing...")
    requests.post(f"https://zenodo.org/api/deposit/depositions/{RECORD_ID}/actions/edit", headers=headers)

    # 2. Upload using the files endpoint instead of bucket (older but sometimes more reliable for certain states)
    print(f"Uploading {METADATA_FILE}...")
    with open(METADATA_FILE, "rb") as fp:
        files = {'file': fp, 'name': METADATA_FILE}
        r_put = requests.post(f"https://zenodo.org/api/deposit/depositions/{RECORD_ID}/files", files=files, headers=headers)

    if r_put.status_code in [200, 201]:
        print(f"Successfully uploaded {METADATA_FILE} to record {RECORD_ID}!")

        # 3. Publish
        print("Publishing changes...")
        r_pub = requests.post(f"https://zenodo.org/api/deposit/depositions/{RECORD_ID}/actions/publish", headers=headers)
        if r_pub.status_code in [200, 201, 202]:
            print("Successfully published!")
        else:
            print(f"Error publishing: {r_pub.text}")
    else:
        print(f"Error uploading file: {r_put.text}")

if __name__ == "__main__":
    seed()
