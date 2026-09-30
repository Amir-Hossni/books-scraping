import sqlite3
import pandas as pd


CSV_FILE = "books.csv"
DATABASE_FILE = "books.db"
TABLE_NAME = "books"


def load_books_to_database():
    df = pd.read_csv(CSV_FILE)

    connection = sqlite3.connect(DATABASE_FILE)

    df.to_sql(
        TABLE_NAME,
        connection,
        if_exists="replace",
        index=False,
    )

    connection.close()


def main():
    load_books_to_database()
    print(f"Database created: {DATABASE_FILE}")


if __name__ == "__main__":
    main()