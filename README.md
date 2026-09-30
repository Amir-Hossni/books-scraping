# Books to Scrape — Scraping & SQL Task

Scrapes the first 100 books (pages 1–5) from [books.toscrape.com](https://books.toscrape.com), a site built for scraping practice, saves them to `books.csv`, loads them into SQLite, and answers three SQL questions.

## Project Structure

```
.
├── Scrapper.py        # Part 1 — scrape pages 1–5 into books.csv
├── DataBase.py        # Part 2 — load books.csv into books.db (SQLite)
├── queries.sql        # Part 2 — the three SQL answers
├── EDA.py             # Quick sanity check of books.csv (types, nulls, counts)
├── books.csv          # Output: 100 books
├── books.db           # Output: SQLite database (table: books)
├── requirements.txt
└── .python-version    # Python 3.13
```

## Setup

Requires **Python 3.13**.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## How to Run

```bash
python Scrapper.py     # 1. scrape -> books.csv
python DataBase.py     # 2. load   -> books.db
sqlite3 books.db < queries.sql   # 3. run the queries
```

If the `sqlite3` command-line tool isn't installed, open `books.db` in any SQLite viewer (e.g. DB Browser for SQLite) and run `queries.sql`.

---

## Part 1 — Scrape

Output: [`books.csv`](books.csv) with 100 rows and these columns:

| Column     | Type    | Example                                                                  |
|------------|---------|--------------------------------------------------------------------------|
| `title`    | text    | A Light in the Attic                                                     |
| `price`    | float   | 51.77                                                                    |
| `rating`   | int 1–5 | 3                                                                        |
| `in_stock` | boolean | True                                                                     |
| `url`      | text    | https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html |

How each field is cleaned:

- **price**: the site doesn't declare a charset, so `requests` decodes the page as ISO-8859-1 and `£51.77` arrives as `Â£51.77`. Instead of depending on the currency symbol, the number is extracted with a regex and converted to `float`.
- **rating**: the star rating is stored as a CSS class (`star-rating Three`), which is mapped to `1`–`5`.
- **in_stock**: `True` if the availability text contains "In stock".
- **url**: the relative `href` is resolved against the page it was found on, so it becomes an absolute link.

Before saving, the scraper validates the output: exactly 100 books, the correct set of fields, `price` is a float, `rating` is 1–5, and `in_stock` is a boolean. If any check fails, it stops with an error instead of writing a bad CSV.

## Part 2 — SQL

The queries are in [`queries.sql`](queries.sql). Results from the scraped data:

**1. Average price for each rating**

| rating | average_price |
|-------:|--------------:|
| 1      | 35.52         |
| 2      | 35.91         |
| 3      | 36.84         |
| 4      | 33.98         |
| 5      | 30.01         |

**2. The 5 most expensive books rated 4 or 5**

| title                                                   | price | rating |
|---------------------------------------------------------|------:|-------:|
| The Death of Humanity: and the Case for Life            | 58.11 | 4      |
| The Past Never Ends                                     | 56.50 | 4      |
| Sapiens: A Brief History of Humankind                   | 54.23 | 5      |
| Scott Pilgrim's Precious Little Life (Scott Pilgrim #1) | 52.29 | 5      |
| Behind Closed Doors                                     | 52.22 | 4      |

**3. How many books are out of stock, per rating**

| rating | out_of_stock_count |
|-------:|-------------------:|
| 1      | 0                  |
| 2      | 0                  |
| 3      | 0                  |
| 4      | 0                  |
| 5      | 0                  |

All 100 books on pages 1–5 are in stock. The query counts with `SUM(CASE ...)` instead of filtering with `WHERE in_stock = 0`, so every rating still appears with `0` rather than returning an empty table.

## Part 3 — Five Lines

**What broke, or took longer than expected?**

1. The main issue was a character-encoding problem when parsing the currency symbol in the price field, so I extracted the numeric value with a regex before converting it to float.
2. The book URLs: I first resolved each `href` against the site root instead of the page it came from, which dropped `/catalogue/` and produced 100 links that returned 404. The script still ran without errors because it never requests the book pages, so I caught it by opening the links and now resolve them against the current page URL.
3. The out-of-stock query returned an empty table because every book is in stock, so I moved the condition into `SUM(CASE ...)` to show `0` per rating.

**If the site started blocking you after 50 requests, what would you change?**

4. Slow down and look like one polite client: reuse a `requests.Session`, send a real `User-Agent`, add a randomized delay between requests, and respect `robots.txt`.
5. Handle blocks gracefully: retry `429`/`503` responses with exponential backoff (honoring `Retry-After`), cache pages already fetched so a rerun doesn't repeat requests, and save progress so the scrape can resume where it stopped.
