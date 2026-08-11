import json
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from extractor import extract_book, extract_all_books
from normalizer import normalize_and_validate
from parser import discover_book_urls


OUTPUT_DIR = Path("output")
RUN_REPORT_FILE = OUTPUT_DIR / "run-report.json"

FAKE_BOOK_URL = (
    "https://books.toscrape.com/"
    "catalogue/fake-book-for-stage-5/index.html"
)

FAKE_SOURCE_PAGE = (
    "https://books.toscrape.com/"
    "catalogue/page-1.html"
)


def save_run_report(report):
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RUN_REPORT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )


def run():
    start_time = datetime.now(
        timezone.utc
    )

    timer_start = perf_counter()

    print("Starting Stage 5 scraper run...")
    print()

    raw_books = []
    extraction_stats = {
        "pages_fetched": 0,
        "cache_hits": 0,
        "failures": [],
    }

    try:
        discovered_books = discover_book_urls()

        print()
        print(
            "Adding one deliberate fake URL "
            "for the Stage 5 failure test."
        )

        discovered_books.append(
            (
                FAKE_BOOK_URL,
                FAKE_SOURCE_PAGE,
            )
        )

        print(
            f"Test list size: "
            f"{len(discovered_books)}"
        )
        print()

        for product_url, source_page in discovered_books:

            try:
                record, cache_hit = extract_book(
                    product_url,
                    source_page,
                )

                raw_books.append(record)

                extraction_stats[
                    "pages_fetched"
                ] += 1

                if cache_hit:
                    extraction_stats[
                        "cache_hits"
                    ] += 1

                print(
                    f"Processed "
                    f"{len(raw_books)}/"
                    f"{len(discovered_books)}: "
                    f"{record['title']}"
                )

            except Exception as exc:

                failure = {
                    "product_url": product_url,
                    "source_page": source_page,
                    "error": str(exc),
                }

                extraction_stats[
                    "failures"
                ].append(failure)

                print()
                print(
                    "FAILED PAGE:"
                )
                print(
                    f"URL: {product_url}"
                )
                print(
                    f"Reason: {exc}"
                )
                print(
                    "Continuing with "
                    "the remaining records..."
                )
                print()

        print()
        print(
            "Extraction finished."
        )

        print(
            f"Successful pages: "
            f"{len(raw_books)}"
        )

        print(
            f"Cache hits: "
            f"{extraction_stats['cache_hits']}"
        )

        print(
            f"Failed pages: "
            f"{len(extraction_stats['failures'])}"
        )

        print()
        print(
            "Starting normalization "
            "and validation..."
        )

        valid_records = normalize_and_validate(
            raw_books
        )

    except Exception as exc:

        print()
        print(
            f"Unexpected run failure: {exc}"
        )

        valid_records = []

        extraction_stats[
            "failures"
        ].append(
            {
                "product_url": None,
                "source_page": None,
                "error": str(exc),
            }
        )

    duration_seconds = round(
        perf_counter() - timer_start,
        3,
    )

    report = {
        "started_at": start_time.isoformat(),
        "duration_seconds": duration_seconds,
        "pages_fetched": extraction_stats[
            "pages_fetched"
        ],
        "cache_hits": extraction_stats[
            "cache_hits"
        ],
        "valid_records": len(valid_records),
        "invalid_records": 0,
        "failed_pages": len(
            extraction_stats["failures"]
        ),
        "failures": extraction_stats[
            "failures"
        ],
    }

    save_run_report(report)

    print()
    print("==============================")
    print("RUN REPORT")
    print("==============================")

    print(
        json.dumps(
            report,
            indent=2,
        )
    )

    print()
    print(
        f"Saved report: "
        f"{RUN_REPORT_FILE}"
    )


if __name__ == "__main__":
    run()