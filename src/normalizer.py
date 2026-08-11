import json
import re
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, HttpUrl, ValidationError


OUTPUT_DIR = Path("output")
BOOKS_FILE = OUTPUT_DIR / "books.json"
ERRORS_FILE = OUTPUT_DIR / "errors.json"


class BookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float
    availability_text: Optional[str] = None
    rating_text: Optional[str] = None
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: str


def normalize_price(price_text: str) -> float:
    """
    Convert a price such as '£51.77' into 51.77.
    """

    if not price_text:
        raise ValueError("price_text is empty")

    cleaned = price_text.replace("Â£", "£").strip()

    match = re.search(
        r"£\s*([0-9]+(?:\.[0-9]+)?)",
        cleaned,
    )

    if not match:
        raise ValueError(
            f"Could not extract GBP price from: {price_text!r}"
        )

    return float(match.group(1))


def normalize_record(raw_record: dict) -> dict:
    """
    Convert one raw scraped record into the clean schema.
    """

    price_gbp = normalize_price(
        raw_record.get("price_text", "")
    )

    record = {
        "title": raw_record.get("title"),
        "product_url": raw_record.get("product_url"),
        "price_text": raw_record.get("price_text"),
        "price_gbp": price_gbp,
        "availability_text": raw_record.get(
            "availability_text"
        ),
        "rating_text": raw_record.get(
            "rating_text"
        ),
        "description": raw_record.get(
            "description"
        ),
        "source_page": raw_record.get(
            "source_page"
        ),
        "fetched_at": raw_record.get(
            "fetched_at"
        ),
    }

    return record


def validate_record(record: dict) -> BookRecord:
    """
    Validate one normalized record using Pydantic.
    """

    return BookRecord.model_validate(record)


def save_json(path: Path, data) -> None:
    """
    Save JSON using UTF-8 encoding.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )


def normalize_and_validate(
    raw_records: list[dict],
) -> list[dict]:
    """
    Normalize and validate all raw records.

    Valid records are returned.
    Invalid records are written to errors.json.
    """

    valid_records = []
    errors = []

    seen_urls = set()

    for index, raw_record in enumerate(
        raw_records,
        start=1,
    ):

        try:
            normalized = normalize_record(
                raw_record
            )

            validated = validate_record(
                normalized
            )

            canonical_url = str(
                validated.product_url
            )

            if canonical_url in seen_urls:
                print(
                    f"Duplicate skipped: "
                    f"{canonical_url}"
                )
                continue

            seen_urls.add(canonical_url)

            valid_records.append(
                validated.model_dump(
                    mode="json"
                )
            )

            print(
                f"Validated "
                f"{index}/{len(raw_records)}: "
                f"{validated.title}"
            )

        except (
            ValueError,
            ValidationError,
        ) as exc:

            error_record = {
                "index": index,
                "record": raw_record,
                "error": str(exc),
            }

            errors.append(
                error_record
            )

            print(
                f"INVALID "
                f"{index}/{len(raw_records)}"
            )

    save_json(
        BOOKS_FILE,
        valid_records,
    )

    save_json(
        ERRORS_FILE,
        errors,
    )

    print()
    print(
        f"valid_records={len(valid_records)}"
    )
    print(
        f"invalid_records={len(errors)}"
    )
    print(
        f"books_file={BOOKS_FILE}"
    )
    print(
        f"errors_file={ERRORS_FILE}"
    )

    return valid_records


if __name__ == "__main__":
    print("Normalizer module ready.")