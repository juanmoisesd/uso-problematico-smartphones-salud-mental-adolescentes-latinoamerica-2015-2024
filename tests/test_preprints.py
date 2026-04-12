import os
import glob

def test_manuscripts_exist():
    manuscripts = glob.glob("preprints/manuscripts/*.md")
    assert len(manuscripts) == 10

def test_pdfs_exist():
    pdfs = glob.glob("preprints/pdfs/*.pdf")
    assert len(pdfs) == 10

def test_pdf_naming_convention():
    pdfs = glob.glob("preprints/pdfs/*.pdf")
    for pdf in pdfs:
        filename = os.path.basename(pdf)
        assert filename.startswith("Preprint_Neuro_")
        assert filename.endswith("_JuanMoisesdelaSerna.pdf")

def test_scripts_exist():
    assert os.path.exists("scripts/generate_preprints.py")
    assert os.path.exists("scripts/publish_to_zenodo.py")
