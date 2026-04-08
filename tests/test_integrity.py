import pytest
import os

def test_integrity():
    # Basic integrity check: check if data directories exist
    assert os.path.exists("data/raw")
    assert os.path.exists("data/clean")
    assert os.path.exists("data/analysis_ready")
