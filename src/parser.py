from pathlib import Path
from time import sleep
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
FIRST_PAGE_URL = "https://books.toscrape.com/catalogue/page-1.html"

CACHE_DIR = Path("cache")

HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0"
}

TIMEOUT = 10
DELAY_SECONDS = 0.5


def get_cache_path(page_number):
    return CACHE_DIR / f"catalogue-page-{page_number}.html"


def load_catalogue_page(url, page_number):
    cache_file = get_cache_path(page_number)

    if cache_file.exists():
        print(f"CACHE HIT page {page_number}")
        return cache_file.read_text(encoding="utf-8")

    print(f"FETCH page {page_number}")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch {url}: HTTP {response.status_code}"
        )

    cache_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    cache_file.write_text(
        response.text,
        encoding="utf-8",
    )

    print(
        f"Downloaded HTML characters: {len(response.text)}"
    )

    return response.text


def discover_book_urls():
    current_url = FIRST_PAGE_URL
    book_urls = []
    catalogue_pages = 0

    while current_url and catalogue_pages < 3:
        catalogue_pages += 1

        source_page = current_url

        html = load_catalogue_page(
            current_url,
            catalogue_pages,
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        books = soup.select(
            "article.product_pod h3 a"
        )

        for book in books:
            href = book.get("href")

            if href:
                absolute_url = urljoin(
                    current_url,
                    href,
                )

                book_urls.append(
                    (absolute_url, source_page)
                )

        next_link = soup.select_one(
            "li.next a"
        )

        if next_link:
            next_href = next_link.get("href")

            current_url = urljoin(
                current_url,
                next_href,
            )

            if not get_cache_path(
                catalogue_pages + 1
            ).exists():
                sleep(DELAY_SECONDS)

        else:
            current_url = None

    unique_books = {}

    for product_url, source_page in book_urls:
        if product_url not in unique_books:
            unique_books[product_url] = source_page

    print(
        f"catalogue_pages={catalogue_pages}"
    )

    print(
        f"discovered={len(book_urls)}"
    )

    print(
        f"unique_urls={len(unique_books)}"
    )

    return list(unique_books.items())


if __name__ == "__main__":
    discover_book_urls()