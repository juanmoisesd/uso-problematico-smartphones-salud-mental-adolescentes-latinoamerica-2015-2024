import requests
import json
import os
import sys

# Secret is retrieved from environment variable
TOKEN = os.environ.get("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"

def update_seo(dep_id):
    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        sys.exit(1)

    params = {'access_token': TOKEN}

    print(f"Updating SEO for deposition {dep_id}...")

    # 1. Start editing
    r_edit = requests.post(f"{BASE_URL}/{dep_id}/actions/edit", params=params)
    if r_edit.status_code != 201:
        print(f"  Error starting edit for {dep_id}: {r_edit.text}")
        return

    # 2. Get bucket URL
    r_get = requests.get(f"{BASE_URL}/{dep_id}", params=params)
    bucket_url = r_get.json()['links']['bucket']

    # 3. Upload Optimized Files
    files = ["schema.jsonld", "SEO_OPTIMIZED_METADATA.json"]
    for filename in files:
        if os.path.exists(filename):
            print(f"  Uploading {filename}...")
            with open(filename, "rb") as fp:
                r_put = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)
            if r_put.status_code not in [200, 201]:
                print(f"  Error uploading {filename}: {r_put.text}")
                return

    # 4. Publish
    print("  Publishing updates...")
    r_pub = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params=params)
    if r_pub.status_code == 202:
        print(f"  Successfully updated SEO for {dep_id}!")
    else:
        print(f"  Error publishing updates: {r_pub.text}")

if __name__ == "__main__":
    # Update Model Card and Cross-Walker
    update_seo("19602357")
    update_seo("19602903")
