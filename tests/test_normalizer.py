from src.normalizer import (
    normalize_price,
    normalize_and_validate,
)


def test_normalize_price():
    assert normalize_price("£51.77") == 51.77


def test_normalize_price_with_encoding_issue():
    assert normalize_price("Â£51.77") == 51.77


def test_duplicate_urls_are_skipped():
    records = [
        {
            "title": "Book One",
            "product_url": "https://example.com/book-1",
            "price_text": "£10.00",
            "availability_text": "In stock",
            "rating_text": "Three",
            "description": "A book.",
            "source_page": "https://example.com/page-1",
            "fetched_at": "2026-08-12T10:00:00+00:00",
        },
        {
            "title": "Book One Duplicate",
            "product_url": "https://example.com/book-1",
            "price_text": "£10.00",
            "availability_text": "In stock",
            "rating_text": "Three",
            "description": "A duplicate.",
            "source_page": "https://example.com/page-1",
            "fetched_at": "2026-08-12T10:00:01+00:00",
        },
    ]

    result = normalize_and_validate(records)

    assert len(result) == 1
    assert result[0]["product_url"] == "https://example.com/book-1"


def test_invalid_record_is_rejected():
    records = [
        {
            "title": "Invalid Book",
            "product_url": "not-a-valid-url",
            "price_text": "£10.00",
            "availability_text": "In stock",
            "rating_text": "Three",
            "description": "A book.",
            "source_page": "https://example.com/page-1",
            "fetched_at": "2026-08-12T10:00:00+00:00",
        }
    ]

    result = normalize_and_validate(records)

    assert result == []
