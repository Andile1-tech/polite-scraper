# The Polite Scraper

A small, polite, cached Python web scraper built for the FlyRank Backend Track Week 5 assignment.

The project discovers books from the first three catalogue pages of Books to Scrape, extracts the individual book detail pages, normalizes and validates the data, records failures without stopping the entire run, caches downloaded pages, and includes automated tests.

## Project Goal

The goal of this project is not simply to download HTML.

It demonstrates a complete scraping workflow:

1. Select an appropriate scraping target.
2. Fetch catalogue pages politely.
3. Cache downloaded pages to avoid unnecessary repeat requests.
4. Discover unique product URLs.
5. Fetch individual product pages.
6. Extract structured book information.
7. Normalize values such as GBP prices.
8. Validate records using Pydantic.
9. Handle failed pages without stopping the complete run.
10. Save clean output and a run report.
11. Test important parser and normalization behaviour.

## Target Classification

### Target

[Books to Scrape](https://books.toscrape.com/)

### Why this site?

Books to Scrape is a public demo website specifically created for practicing web scraping.

It is therefore appropriate for this educational assignment.

### Scope

The scraper processes only the first three catalogue pages.

Those pages contain:

- 3 catalogue pages
- 60 discovered books
- 60 unique product URLs

The project intentionally keeps the scope small rather than crawling the entire website.

## Data Collected

For each book, the scraper collects:

- `title`
- `product_url`
- `price_text`
- `availability_text`
- `rating_text`
- `description`
- `source_page`
- `fetched_at`

During normalization, the original price text is also converted into:

- `price_gbp`

For example:

```text
£51.77
```

## How the Scraper Works

The scraper follows this pipeline:

Catalogue pages
      |
      v
Cache / HTTP fetch
      |
      v
Book URL discovery
      |
      v
Individual book pages
      |
      v
Data extraction
      |
      v
Normalization
      |
      v
Validation
      |
      v
JSON output + run report

## Target Classification

[Books to Scrape](https://books.toscrape.com/)

### Why This Site?

Books to Scrape is a public demo website specifically created for practicing web scraping.

It is therefore appropriate for this educational assignment.

### Scope

The scraper processes only the first three catalogue pages.

Expected scope:

- 3 catalogue pages
- 60 discovered books
- 60 unique product URLs

The project intentionally keeps the scope small rather than crawling the entire website.

## Record Schema

Each normalized book record contains:

- `title`
- `product_url`
- `price_text`
- `price_gbp`
- `availability_text`
- `rating_text`
- `description`
- `source_page`
- `fetched_at`

## Politeness Rules

The scraper uses:

- a descriptive User-Agent
- a 10-second request timeout
- a delay between requests
- local caching to avoid unnecessary repeat requests
- retry handling for temporary server failures

HTTP 403 and 404 responses are treated as non-retryable failures.

## Author

**Andile Mnikina**

Backend AI Engineer | Python Developer

Built as part of the FlyRank Backend Track assignment.

GitHub: https://github.com/Andile1-tech