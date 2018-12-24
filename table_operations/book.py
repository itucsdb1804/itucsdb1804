import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import BookObj


class Book(baseClass):
    def __init__(self):
        super().__init__("BOOK", BookObj)

    def add_book(self, book):
        query = "INSERT INTO BOOK (BOOK_NAME, RELEASE_YEAR, BOOK_EXPLANATION) VALUES (%s, %s, %s) RETURNING BOOK_ID"
        fill = (book.book_name, book.release_year, book.explanation)

        last_book_id = (self.execute(query, fill, True))[0][0]

        return last_book_id if last_book_id is not None else -1

    def update(self, book_key, book):
        query = "UPDATE BOOK SET BOOK_NAME = %s, RELEASE_YEAR = %s, BOOK_EXPLANATION = %s WHERE BOOK_ID = %s"
        fill = (book.book_name, book.release_year, book.explanation, book_key)
        self.execute(query, fill)

        return book_key

    def delete(self, book_key):
        query1 = "DELETE FROM BOOK_AUTHOR WHERE BOOK_ID = %s"
        query2 = "DELETE FROM BOOK_CATEGORY WHERE BOOK_ID = %s"
        query3 = "DELETE FROM BOOK WHERE BOOK_ID = %s"
        fill = (book_key, )
        self.execute(query1, fill)
        self.execute(query2, fill)
        self.execute(query3, fill)

    def get_row(self, book_key):
        return super().get_row("*", ["BOOK_ID"], [book_key])
