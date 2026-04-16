import requests
import os
import sys

def create_master_record(token, files_to_upload):
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "https://zenodo.org/api"

    print("Creating master record for Atlas de Salud Mental Migratoria...")

    # Metadata for the new record
    # Removed communities as it might cause 500 if not authorized or misspelled
    metadata = {
        "metadata": {
            "title": "Atlas de Salud Mental Migratoria (JMS-Atlas) - Humanitarian AI Wiki & Mapping",
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": "Master record for Cluster #3: Mental Health & Accessibility in Migratory Processes. Includes the Humanitarian AI Guide and JSON-LD mapping to World Bank/IOM indicators.",
            "creators": [{"name": "De la Serna, Juan Moisés", "affiliation": "Universidad Internacional de La Rioja (UNIR)"}],
            "keywords": ["Migración", "Salud Mental", "Empatía Algorítmica", "Duelo Migratorio", "Humanitarian AI"],
            "license": "cc-by-4.0",
            "access_right": "open"
        }
    }

    # Step 1: Create deposition
    r = requests.post(f"{base_url}/deposit/depositions", json=metadata, headers=headers)
    if r.status_code != 201:
        print(f"Failed to create deposition: {r.status_code}")
        print(r.text)
        sys.exit(1)

    deposition = r.json()
    dep_id = deposition['id']
    bucket_url = deposition['links']['bucket']
    print(f"Deposition created: {dep_id}")

    # Step 2: Upload files
    for filepath in files_to_upload:
        filename = os.path.basename(filepath)
        print(f"Uploading {filename}...")
        with open(filepath, "rb") as fp:
            r = requests.put(f"{bucket_url}/{filename}", data=fp, headers=headers)
            if r.status_code not in [200, 201]:
                print(f"Failed to upload {filename}: {r.status_code}")
                sys.exit(1)

    # Step 3: Publish
    print("Publishing...")
    r = requests.post(f"{base_url}/deposit/depositions/{dep_id}/actions/publish", headers=headers)
    if r.status_code != 202:
        print(f"Failed to publish: {r.status_code}")
        print(r.text)
        sys.exit(1)

    published = r.json()
    print(f"Master Record Published! DOI: {published.get('doi')}")
    print(f"URL: {published['links']['record_html']}")

if __name__ == "__main__":
    TOKEN = os.getenv("ZENODO_TOKEN")
    FILES = ["migration_impact_mapping.jsonld", "HUMANITARIAN_AI_GUIDE.md"]
    create_master_record(TOKEN, FILES)
