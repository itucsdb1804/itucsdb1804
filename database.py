from tables import *
import psycopg2 as dbapi2
import os
import sys


class Database:
    def __init__(self):
        url = os.getenv("DATABASE_URL")
        if url is None:
            print("Usage: DATABASE_URL=url python database.py", file=sys.stderr)
            sys.exit(1)
        self.book = self.Book(url)

    # myilmaz
    class Book:
        def __init__(self, url):
            self.url = url

        def add_book(self, book):
            query = "INSERT INTO BOOK (BOOK_NAME, RELEASE_YEAR, EXPLANATION) VALUES (%s, %s, %s)"
            fill = (book.book_name, book.release_year, book.explanation)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, book_key, book):
            query = "UPDATE BOOK SET BOOK_NAME = %s, RELEASE_YEAR = %s, EXPLANATION = %s WHERE BOOK_ID = %s"
            # TODO book_key or book.book_id
            fill = (book.book_name, book.release_year, book.explanation, book_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, book_key):
            query = "DELETE FROM BOOK WHERE BOOK_ID = %s"
            fill = (book_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, book_key):
            _book = None

            query = "SELECT * FROM BOOK WHERE BOOK_ID = %s"
            fill = (book_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                book = cursor.fetchone()
                if book is not None:
                    _book = Book(book[1], book[2], book[3])

            return _book

        def get_table(self):
            books = []

            query = "SELECT * FROM BOOK;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for book in cursor:
                    book_ = Book(book[1], book[2], book[3])
                    books.append((book[0], book_))
                cursor.close()

            return books