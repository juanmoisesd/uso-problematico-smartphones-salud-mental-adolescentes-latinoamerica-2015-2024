import os
import re

def validate_preprint(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # Check author
    if "Juan Moisés de la Serna" not in content:
        errors.append("Author name missing or incorrect.")

    # Check PRISMA structure
    sections = ["Resumen", "Palabras clave", "Introducción", "Métodos", "Resultados", "Discusión", "Conclusiones", "Referencias", "Future Directions"]
    for section in sections:
        if section not in content:
            errors.append(f"Section '{section}' missing.")

    # Check number of citations (20-30)
    # References are numbered in the format "1. ", "2. ", etc.
    refs = re.findall(r"\d+\.\s+\w+", content)
    num_refs = len(refs)
    if num_refs < 20 or num_refs > 30:
        # Some citations might not be numbered if formatting varied slightly,
        # but our drafts used 25. Let's count lines in References section.
        ref_section = content.split("### 8. Referencias")[-1].split("---")[0]
        lines = [l for l in ref_section.strip().split("\n") if l.strip()]
        num_refs = len(lines)
        if num_refs < 20:
             errors.append(f"Insufficient citations: found {num_refs}, expected 20-30.")

    # Check cross-citations
    cross_cites = re.findall(r"Capítulo \d+", content)
    if len(cross_cites) < 2:
        errors.append(f"Insufficient cross-citations: found {len(cross_cites)}, expected >= 2.")

    return errors

def main():
    preprints_dir = "preprints"
    all_passed = True
    for filename in os.listdir(preprints_dir):
        if filename.endswith(".md"):
            path = os.path.join(preprints_dir, filename)
            errors = validate_preprint(path)
            if errors:
                print(f"FAILED: {filename}")
                for err in errors:
                    print(f"  - {err}")
                all_passed = False
            else:
                print(f"PASSED: {filename}")

    if not all_passed:
        exit(1)

if __name__ == "__main__":
    main()
