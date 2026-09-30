
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://books.toscrape.com/"

PAGE_URL_PATTERN = "catalogue/page-{page_number}.html"
BOOK_SELECTOR = "article.product_pod"

EXPECTED_BOOKS = 100
START_PAGE = 1
END_PAGE = 5
OUTPUT_FILE = "books.csv"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_book(book_element, page_url):
    title_link = book_element.select_one("h3 a")

    title = title_link["title"]

    price_text = book_element.select_one("p.price_color").get_text(strip=True)
    price = float(re.search(r"\d+\.\d+", price_text).group())

    rating_element = book_element.select_one("p.star-rating")
    rating_word = rating_element.get("class")[1]
    rating = RATING_MAP[rating_word]

    stock_text = book_element.select_one(
        "p.instock.availability"
    ).get_text(strip=True)
    in_stock = "In stock" in stock_text

    relative_url = title_link["href"]
    # href is relative to the page it appears on (catalogue/), not the site root
    url = urljoin(page_url, relative_url)

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "in_stock": in_stock,
        "url": url,
    }


def scrape_books():
    books = []

    for page_number in range(START_PAGE, END_PAGE + 1):
        page_url = urljoin(BASE_URL, PAGE_URL_PATTERN.format(page_number=page_number))

        print(f"Scraping page {page_number}: {page_url}")

        html = fetch_page(page_url)
        soup = BeautifulSoup(html, "html.parser")

        book_elements = soup.select(BOOK_SELECTOR)

        for book_element in book_elements:
            book = parse_book(book_element, page_url)
            books.append(book)

    return books


def validate_books(books, expected_count):
    if len(books) != expected_count:
        raise ValueError(
            f"Expected {expected_count} books, but found {len(books)}."
        )

    required_fields = {
        "title",
        "price",
        "rating",
        "in_stock",
        "url",
    }

    for book in books:
        if set(book.keys()) != required_fields:
            raise ValueError("Book has an invalid set of fields.")

        if not isinstance(book["price"], float):
            raise TypeError("Price must be a float.")

        if book["rating"] not in range(1, 6):
            raise ValueError("Rating must be between 1 and 5.")

        if not isinstance(book["in_stock"], bool):
            raise TypeError("in_stock must be a boolean.")


def save_to_csv(books):
    df = pd.DataFrame(books)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


def main():
    books = scrape_books()

    validate_books(books, EXPECTED_BOOKS)

    save_to_csv(books)

    print(f"\nSuccessfully scraped {len(books)} books.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()