import os
import json

def test_model_card_exists():
    assert os.path.exists("MODEL_CARD.md")

def test_license_exists():
    assert os.path.exists("LICENSE.txt")

def test_schema_jsonld_exists():
    assert os.path.exists("schema.jsonld")

def test_schema_jsonld_valid():
    with open("schema.jsonld", "r") as f:
        data = json.load(f)
    assert data["@context"] == "https://schema.org/"
    assert data["@type"] == "Dataset"

def test_model_card_template_correct():
    with open("MODEL_CARD.md", "r") as f:
        content = f.read()
    assert "[TU_DOI]" in content
