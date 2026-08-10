from pathlib import Path

import requests


URL = "https://books.toscrape.com/catalogue/page-1.html"
CACHE_FILE = Path("cache/catalogue-page-1.html")

HEADERS = {
    "User-Agent": "PoliteScraper/1.0 (educational assignment)"
}


def fetch_page():
    # If we already downloaded this page, use the local copy.
    if CACHE_FILE.exists():
        print("CACHE HIT")
        return CACHE_FILE.read_text(encoding="utf-8")

    # The page is not cached, so make one request.
    print("FETCH")

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=10,
    )

    # Stop if the server returned an unsuccessful HTTP status.
    response.raise_for_status()

    # Make sure the cache folder exists.
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save the downloaded HTML locally.
    CACHE_FILE.write_text(
        response.text,
        encoding="utf-8",
    )

    return response.text


if __name__ == "__main__":
    html = fetch_page()
    print(f"Downloaded HTML characters: {len(html)}")