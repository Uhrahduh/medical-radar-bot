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
    ("Helios Wuppertal", "https://www.helios-gesundheit.de/karriere/")
]

def scan_jobs():
    results = []

    for name, url in HOSPITALS:
        try:
            r = requests.get(url, timeout=10)

            text = BeautifulSoup(r.text, "html.parser").get_text().lower()

            if any(k in text for k in KEYWORDS):
                results.append(
                    f"🏥 {name}\n🔗 {url}"
                )

        except:
            pass

    return results
