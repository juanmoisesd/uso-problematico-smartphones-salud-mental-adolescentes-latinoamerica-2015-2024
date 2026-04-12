import os
import glob

def test_manuscripts_exist():
    es = glob.glob("preprints/manuscripts/*.md")
    en = glob.glob("preprints/manuscripts_en/*.md")
    assert len(es) == 10
    assert len(en) == 10

def test_pdfs_exist():
    es = glob.glob("preprints/pdfs/*.pdf")
    en = glob.glob("preprints/pdfs_en/*.pdf")
    assert len(es) == 10
    assert len(en) == 10

def test_pdf_naming_convention():
    pdfs = glob.glob("preprints/pdfs/*.pdf") + glob.glob("preprints/pdfs_en/*.pdf")
    for pdf in pdfs:
        filename = os.path.basename(pdf)
        assert filename.startswith("Preprint_Neuro_")
        assert filename.endswith("_JuanMoisesdelaSerna.pdf")

def test_scripts_exist():
    assert os.path.exists("scripts/generate_preprints.py")
    assert os.path.exists("scripts/publish_to_zenodo.py")
    assert os.path.exists("scripts/publish_to_zenodo_en.py")
