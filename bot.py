import requests
from bs4 import BeautifulSoup
import hashlib

KEYWORDS = [
    "assistenzarzt",
    "assistenzärztin",
    "arzt in weiterbildung",
    "weiterbildung"
]

SPECIALTY_HINTS = [
    "anästhesie",
    "radiologie",
    "chirurgie",
    "kardiologie",
    "geriatrie",
    "innere"
]

HOSPITALS = [
    ("UK Essen", "https://www.uk-essen.de/karriere/stellenangebote/"),
    ("Klinikum Dortmund", "https://www.klinikumdo.de/karriere/"),
    ("Helios Wuppertal", "https://www.helios-gesundheit.de/karriere/"),
    ("Klinikum Bochum", "https://www.klinikum-bochum.de/karriere/"),
    ("Klinikum Duisburg", "https://www.klinikum-duisburg.de/karriere/"),
    ("Klinikum Düsseldorf", "https://www.klinikum-duesseldorf.de/karriere/"),
]

seen = set()


def hash_job(text):
    return hashlib.md5(text.encode()).hexdigest()


def detect_specialty(text):
    t = text.lower()
    for s in SPECIALTY_HINTS:
        if s in t:
            return s
    return "general"


def scan_jobs():
    results = []

    for hospital, url in HOSPITALS:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            links = soup.find_all("a")

            for link in links:
                text = link.get_text(strip=True)
                href = link.get("href")

                if not text or not href:
                    continue

                combined = f"{text} {href}".lower()

                # filtro médico real
                if not any(k in combined for k in KEYWORDS):
                    continue

                job_id = hash_job(combined)

                if job_id in seen:
                    continue

                seen.add(job_id)

                specialty = detect_specialty(combined)

                results.append(
                    f"🏥 {hospital}\n"
                    f"🩺 {specialty}\n"
                    f"📄 {text}\n"
                    f"🔗 {href if href.startswith('http') else url}"
                )

        except:
            continue

    return results
