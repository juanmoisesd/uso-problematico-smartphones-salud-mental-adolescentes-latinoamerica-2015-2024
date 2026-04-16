import json
import os

def test_schema_jsonld_seo():
    assert os.path.exists("schema.jsonld")
    with open("schema.jsonld", "r") as f:
        data = json.load(f)

    # Google Dataset Search critical fields
    assert "name" in data
    assert "description" in data
    assert "variableMeasured" in data
    assert "creator" in data
    assert "distribution" in data

def test_seo_graph_validity():
    assert os.path.exists("SEO_OPTIMIZED_METADATA.json")
    with open("SEO_OPTIMIZED_METADATA.json", "r") as f:
        data = json.load(f)

    assert "@graph" in data
    assert len(data["@graph"]) > 0
