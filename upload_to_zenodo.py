import requests
import json
import os

ZENODO_TOKEN = os.getenv("ZENODO_TOKEN")
BASE_URL = "https://zenodo.org/api/deposit/depositions"

def upload_to_zenodo(pdf_file, title, description):
    if not ZENODO_TOKEN:
        print("ZENODO_TOKEN not set")
        return None, None

    headers = {"Content-Type": "application/json"}
    params = {'access_token': ZENODO_TOKEN}

    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': description,
            'creators': [{'name': 'de la Serna, Juan Moisés', 'affiliation': 'Universidad Internacional de La Rioja (UNIR)', 'orcid': '0000-0002-8401-8018'}],
            'license': 'cc-by-4.0',
            'language': 'spa',
            'access_right': 'open'
        }
    }

    r = requests.post(BASE_URL, params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.status_code} {r.text}")
        return None, None

    deposition_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']

    filename = os.path.basename(pdf_file)
    with open(pdf_file, "rb") as fp:
        upload_url = f"{bucket_url}/{filename}"
        r = requests.put(upload_url, data=fp, params=params)

    if r.status_code not in [200, 201]:
        r = requests.post(f"{BASE_URL}/{deposition_id}/files", params=params, files={'file': open(pdf_file, 'rb')})
        if r.status_code not in [200, 201]:
             return None, None

    r = requests.post(f"{BASE_URL}/{deposition_id}/actions/publish", params=params)
    if r.status_code != 202:
        return None, None

    doi = r.json().get('doi')
    record_url = r.json().get('links', {}).get('record_html')
    return doi, record_url

def main():
    chapters = {
        1: ("El instinto numérico: Cómo el cerebro nace para contar", "Policy brief sobre la percepción innata de las cantidades que compartimos con otros animales."),
        2: ("La geografía del cálculo: Qué áreas cerebrales se encienden ante un problema matemático", "Un recorrido por la corteza parietal, el lóbulo frontal y las redes neuronales involucradas."),
        3: ("De los bloques a las ecuaciones: La neurociencia del aprendizaje matemático infantil", "Cómo el cerebro pasa de entender objetos físicos a conceptualizar números abstractos."),
        4: ("El duelo cerebral: Intuición rápida versus lógica analítica", "Exploración de cómo el cerebro resuelve problemas usando el Sistema 1 (rápido) frente al Sistema 2 (lento y metódico)."),
        5: ("El atajo de la memoria: Cómo el cerebro almacena fórmulas y automatiza el cálculo", "Por qué la práctica matemática cambia la estructura física de las conexiones neuronales."),
        6: ("La amígdala y el pánico a los números: Entendiendo la ansiedad matemática", "La explicación neurológica de por qué las matemáticas generan miedo y estrés real en algunas personas."),
        7: ("El cerebro desconectado: Qué es la discalculia y cómo se manifiesta en la red neuronal", "Un acercamiento empático y científico a las dificultades específicas del aprendizaje matemático."),
        8: ("El gimnasio mental: Neuroplasticidad y estrategias para potenciar tu cerebro lógico", "Consejos basados en ciencia sobre cómo entrenar el cerebro para mejorar en matemáticas a cualquier edad."),
        9: ("Anatomía de un genio: ¿Qué hace diferente al cerebro de los grandes matemáticos?", "Un análisis de los estudios neurocientíficos realizados a mentes brillantes como las de Ramanujan o Einstein."),
        10: ("La sinfonía neuronal: Por qué las matemáticas son el lenguaje oculto del cerebro", "Una reflexión final sobre cómo la estructura del universo y la arquitectura de nuestras neuronas están conectadas.")
    }

    files = {
        1: "Instinto_Numerico",
        2: "Geografia_Calculo",
        3: "Bloques_Ecuaciones",
        4: "Duelo_Cerebral",
        5: "Atajo_Memoria",
        6: "Amigdala_Panico",
        7: "Cerebro_Desconectado",
        8: "Gimnasio_Mental",
        9: "Anatomia_Genio",
        10: "Sinfonia_Neuronal"
    }

    for i in range(1, 11):
        title, desc = chapters[i]
        filename = f"Preprint_Neuro_{files[i]}_JuanMoisesdelaSerna.pdf"
        if not os.path.exists(filename):
            continue

        print(f"Uploading {filename}...")
        doi, url = upload_to_zenodo(filename, f"Policy Brief: {title}", desc)
        if doi:
            print(f"Successfully uploaded! DOI: {doi}")

if __name__ == "__main__":
    main()
