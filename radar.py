import requests
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
