import pytest
import os

def test_schema_exists():
    assert os.path.exists("schema.json")

def test_data_dictionary_exists():
    assert os.path.exists("data_dictionary.csv")
