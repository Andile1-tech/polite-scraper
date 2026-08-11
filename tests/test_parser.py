from src.parser import discover_book_urls


def test_discover_book_urls():
    books = discover_book_urls()

    assert len(books) == 60

    product_urls = [product_url for product_url, source_page in books]

    assert len(set(product_urls)) == 60

    assert all(product_url.startswith("https://") for product_url in product_urls)

    assert all(source_page.startswith("https://") for product_url, source_page in books)
