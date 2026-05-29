import requests
from bs4 import BeautifulSoup

SPECIALTIES = [
    "anästhesiologie",
    "intensivmedizin",
    "radiologie",
    "chirurgie",
    "kardiologie",
    "geriatrie",
    "innere medizin"
]

KEY_TITLES = [
    "assistenzarzt",
    "assistenzärztin",
    "arzt in weiterbildung",
    "weiterbildung"
]

HOSPITALS = [
    ("UK Essen", "https://www.uk-essen.de/karriere/stellenangebote/"),
    ("Klinikum Dortmund", "https://www.klinikumdo.de/karriere/"),
    ("Helios Wuppertal", "https://www.helios-gesundheit.de/karriere/"),
    ("Klinikum Bochum", "https://www.klinikum-bochum.de/karriere/"),
    ("Klinikum Duisburg", "https://www.klinikum-duisburg.de/karriere/"),
    ("Klinikum Düsseldorf", "https://www.klinikum-duesseldorf.de/karriere/"),
    ("Klinikum Wuppertal", "https://www.klinikum-wuppertal.de/karriere/"),
    ("Klinikum Krefeld", "https://www.krankenhaus-krefeld.de/karriere/"),
]

seen = set()


def extract_job_blocks(text):
    """
    Intenta detectar estructura de oferta real:
    separa bloques de texto grandes (no solo keywords)
    """
    return text.split("\n\n")


def is_valid_job(block):
    block_lower = block.lower()

    has_title = any(t in block_lower for t in KEY_TITLES)
    has_specialty = any(s in block_lower for s in SPECIALTIES)

    return has_title and has_specialty


def detect_specialty(block):
    block_lower = block.lower()

    for s in SPECIALTIES:
        if s in block_lower:
            return s

    return "sin especialidad"


def scan_jobs():
    results = []

    for hospital, url in HOSPITALS:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            text = soup.get_text("\n")

            blocks = extract_job_blocks(text)

            for block in blocks:
                if is_valid_job(block):

                    job_id = f"{hospital}-{block[:40]}"

                    if job_id in seen:
                        continue

                    seen.add(job_id)

                    specialty = detect_specialty(block)

                    results.append(
                        f"🏥 {hospital}\n"
                        f"🩺 {specialty}\n"
                        f"🔗 {url}"
                    )

        except:
            continue

    return results
