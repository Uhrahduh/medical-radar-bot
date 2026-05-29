import requests
from bs4 import BeautifulSoup
import hashlib

SPECIALTIES = {
    "anästhesiologie": ["anästhesiologie", "intensivmedizin"],
    "radiologie": ["radiologie"],
    "chirurgie": ["chirurgie"],
    "kardiologie": ["kardiologie", "innere medizin"],
    "geriatrie": ["geriatrie", "innere medizin"]
}

KEYWORDS = [
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
    ("Klinikum Krefeld", "https://www.krankenhaus-krefeld.de/karriere/")
]

seen = set()


def hash_job(text):
    return hashlib.md5(text.encode()).hexdigest()


def detect_specialty(text):
    text = text.lower()

    for main, keys in SPECIALTIES.items():
        if any(k in text for k in keys):
            return main

    return "no-especificado"


def is_valid(text):
    t = text.lower()
    return any(k in t for k in KEYWORDS)


def scan_jobs():
    results = []

    for hospital, url in HOSPITALS:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            blocks = soup.get_text("\n").split("\n\n")

            for b in blocks:
                if not is_valid(b):
                    continue

                job_hash = hash_job(b)

                if job_hash in seen:
                    continue

                seen.add(job_hash)

                specialty = detect_specialty(b)

                results.append(
                    f"🏥 {hospital}\n"
                    f"🩺 {specialty}\n"
                    f"📄 Assistenzarzt Job detectado\n"
                    f"🔗 {url}"
                )

        except:
            continue

    return resultsimport requests
from bs4 import BeautifulSoup

KEYWORDS = [
    "assistenzarzt",
    "arzt in weiterbildung",
    "weiterbildung",
    "anästhesiologie",
    "radiologie",
    "chirurgie",
    "kardiologie",
    "geriatrie"
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

def scan_jobs():
    results = []

    for name, url in HOSPITALS:
        try:
            r = requests.get(url, timeout=10)
            text = BeautifulSoup(r.text, "html.parser").get_text().lower()

            if any(k in text for k in KEYWORDS):
                job_id = f"{name}-{url}"

                if job_id not in seen:
                    seen.add(job_id)

                    results.append(
                        f"🏥 {name}\n🔗 {url}"
                    )

        except:
            continue

    return results
