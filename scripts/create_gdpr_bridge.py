import requests
import json
import os

# Script to create the EUR-Lex/GDPR Cognitive Compliance Bridge on Zenodo

TOKEN = os.environ.get("ZENODO_TOKEN")
COMMUNITY = "jmdeiserna-master"
FILES = ["LEGAL_SEMANTICS.json", "JMS-02_Cognitive_Compliance.md"]

def create_gdpr_bridge():
    if not TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return

    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

    # 1. Create Deposition
    data = {
        'metadata': {
            'title': "Technical Specification for Cognitive Accessibility in Data Protection (Standard JMS-02)",
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': "Standard JMS-02 defines the technical implementation layer for GDPR transparency through cognitive metrics. It includes the LEGAL_SEMANTICS.json glossary for AI-driven legal compliance and neuroscientific validation of informed consent.",
            'creators': [{
                'name': 'de la Serna, Juan Moisés',
                'affiliation': 'Cátedra de Neuroeconomía Forense / UNIR',
                'orcid': '0000-0002-8401-8018'
            }],
            'communities': [{'identifier': COMMUNITY}],
            'license': 'cc-by-4.0',
            'access_right': 'open',
            'keywords': ["GDPR", "Transparency", "Cognitive Accessibility", "Neuroscience", "Consent", "Compliance", "EUR-Lex"],
            'related_identifiers': [
                {
                    'identifier': 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679',
                    'relation': 'isSupplementedBy',
                    'resource_type': 'publication',
                    'scheme': 'url'
                },
                {
                    'identifier': '10.5281/zenodo.19602964',
                    'relation': 'isContinuedBy',
                    'scheme': 'doi'
                }
            ]
        }
    }

    print("Creating GDPR bridge deposition...")
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
        print(f"Successfully published GDPR Bridge! DOI: {doi}")
    else:
        print(f"Error publishing: {r_pub.text}")

if __name__ == "__main__":
    create_gdpr_bridge()
