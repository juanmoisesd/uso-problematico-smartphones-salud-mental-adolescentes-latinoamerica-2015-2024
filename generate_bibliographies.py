import json
import os

def format_bibliography(topic_index, all_topics):
    topic = all_topics[topic_index]
    refs = topic['refs']

    # Add cross-citations (cite 2-3 other preprints)
    # To keep it deterministic, pick the next 2 topics in the list (circular)
    cross_indices = [(topic_index + 1) % len(all_topics), (topic_index + 2) % len(all_topics)]

    formatted_refs = []
    for ref in refs:
        formatted_refs.append(ref)

    for idx in cross_indices:
        other = all_topics[idx]
        cross_ref = f"de la Serna, J. M. (2026). {other['title']}. Zenodo. [Preprint]"
        formatted_refs.append(cross_ref)

    # Sort bibliography alphabetically
    formatted_refs.sort()

    return "\n".join(formatted_refs)

# Load metadata
if __name__ == "__main__":
    with open('metadata/preprints_metadata.json', 'r') as f:
        topics = json.load(f)

    for i, topic in enumerate(topics):
        bib = format_bibliography(i, topics)
        filename = f"metadata/{topic['id']}_bib.txt"
        with open(filename, 'w') as f:
            f.write(bib)

    print("Bibliographies with cross-citations generated.")
