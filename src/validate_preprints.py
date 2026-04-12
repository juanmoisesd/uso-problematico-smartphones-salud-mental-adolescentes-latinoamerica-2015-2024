import os
import re

def validate_preprint(filepath, lang="es"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # Check author
    if "Juan Moisés de la Serna" not in content:
        errors.append("Author name missing or incorrect.")

    # Check PRISMA structure
    if lang == "es":
        sections = ["Resumen", "Palabras clave", "Introducción", "Métodos", "Resultados", "Discusión", "Conclusiones", "Referencias", "Future Directions"]
    elif lang == "fr":
        sections = ["Résumé", "Mots-clés", "Introduction", "Méthodes", "Résultats", "Discussion", "Conclusions", "Références", "Future Directions"]
    else:
        sections = ["Abstract", "Keywords", "Introduction", "Methods", "Results", "Discussion", "Conclusions", "References", "Future Directions"]

    for section in sections:
        if section not in content:
            errors.append(f"Section '{section}' missing.")

    # Check number of citations (20-30 for ES, 30+ for EN/FR)
    if lang == "es":
        ref_header = "### 8. Referencias"
    elif lang == "fr":
        ref_header = "### 8. Références"
    else:
        ref_header = "### 8. References"

    if ref_header in content:
        ref_section = content.split(ref_header)[-1].split("---")[0]
        lines = [l for l in ref_section.strip().split("\n") if l.strip() and re.match(r"\d+\.", l.strip())]
        num_refs = len(lines)
        min_refs = 20 if lang == "es" else 30
        if num_refs < min_refs:
             errors.append(f"Insufficient citations: found {num_refs}, expected >= {min_refs}.")
    else:
        errors.append(f"References header '{ref_header}' missing.")

    # Check cross-citations
    if lang == "es":
        cite_pattern = r"Capítulo \d+"
    elif lang == "fr":
        cite_pattern = r"Chapitre \d+"
    else:
        cite_pattern = r"Chapter \d+"

    cross_cites = re.findall(cite_pattern, content)
    if len(cross_cites) < 2:
        errors.append(f"Insufficient cross-citations: found {len(cross_cites)}, expected >= 2.")

    return errors

def validate_dir(lang):
    preprints_dir = f"preprints/{lang}"
    if not os.path.exists(preprints_dir):
        return True

    all_passed = True
    for filename in os.listdir(preprints_dir):
        if filename.endswith(".md"):
            path = os.path.join(preprints_dir, filename)
            errors = validate_preprint(path, lang=lang)
            if errors:
                print(f"FAILED [{lang}]: {filename}")
                for err in errors:
                    print(f"  - {err}")
                all_passed = False
            else:
                print(f"PASSED [{lang}]: {filename}")
    return all_passed

def main():
    es_ok = validate_dir("es")
    en_ok = validate_dir("en")
    fr_ok = validate_dir("fr")

    if not (es_ok and en_ok and fr_ok):
        exit(1)

if __name__ == "__main__":
    main()
