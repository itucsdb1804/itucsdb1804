import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import BookObj


class Book(baseClass):
    def __init__(self):
        super().__init__("BOOK", BookObj)

    def add_book(self, book):
        query = "INSERT INTO BOOK (BOOK_NAME, RELEASE_YEAR, BOOK_EXPLANATION) VALUES (%s, %s, %s)"
        fill = (book.book_name, book.release_year, book.explanation)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return self.get_table()[-1].book_id

    def update(self, book_key, book):
        query = "UPDATE BOOK SET BOOK_NAME = %s, RELEASE_YEAR = %s, BOOK_EXPLANATION = %s WHERE BOOK_ID = %s"
        fill = (book.book_name, book.release_year, book.explanation, book_key)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return book_key

    def delete(self, book_key):

        query1 = "DELETE FROM BOOK_AUTHOR WHERE BOOK_ID = %s"
        query2 = "DELETE FROM BOOK_CATEGORY WHERE BOOK_ID = %s"
        query3 = "DELETE FROM BOOK WHERE BOOK_ID = %s"
        fill = (book_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query1, fill)
            cursor.execute(query2, fill)
            cursor.execute(query3, fill)
            cursor.close()

    def get_row(self, book_key):
        _book = None

        query = "SELECT * FROM BOOK WHERE BOOK_ID = %s"
        fill = (book_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            book = cursor.fetchone()
            if book is not None:
                _book = BookObj(book[0], book[1], book[2], book[3])

        return _book

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)
