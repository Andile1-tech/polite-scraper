# The Polite Scraper

A small Python web scraper built for the FlyRank Backend Track Week 5 assignment.

## Target Classification

### Target
[Books to Scrape](https://books.toscrape.com/)

### Why this site?
Books to Scrape is a public demo website created for web scraping practice. The website itself states that it is a demo website for web scraping purposes.

### Scope
This scraper will process only the first three catalogue pages and discover the 60 unique books listed across those pages.

### Data collected
For each book, the scraper will collect:

- title
- product_url
- price_text
- availability_text
- rating_text
- description
- source_page
- fetched_at

The cleaned records will also contain a numeric `price_gbp` value.

### Robots check
The requested `https://books.toscrape.com/robots.txt` returned HTTP 404 Not Found.

Therefore, no robots file was found. A missing robots.txt file is not treated as permission to scrape.

### Appropriate use
This target is appropriate for this assignment because Books to Scrape is specifically provided as a public practice sandbox for learning web scraping.

I will not reuse this code on another site without checking its rules and terms first.