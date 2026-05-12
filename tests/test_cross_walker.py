import os
import json

def test_json_validity():
    files = ["ONTOLOGY_MAPPING.json", "METADATA_BENCHMARK.json", "COLLECTION_MASTER.sidecar.json"]
    for f in files:
        assert os.path.exists(f)
        with open(f, "r") as fp:
            data = json.load(fp)
            assert data is not None

def test_ontology_mapping_content():
    with open("ONTOLOGY_MAPPING.json", "r") as f:
        data = json.load(f)
    assert "WHO ICD-11" in str(data)
    assert "6C51" in str(data)

def test_readme_updated():
    with open("README.md", "r") as f:
        content = f.read()
    assert "10.5281/zenodo.19602903" in content
