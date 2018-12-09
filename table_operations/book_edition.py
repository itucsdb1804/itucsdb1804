from table_operations.baseClass import baseClass
from tables import BookEditionObj
import psycopg2 as dbapi2

class BookEdition(baseClass):
    def __init__(self):
        super().__init__("BOOK_EDITION", BookEditionObj)

    def add(self, book_edition):
        query = "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        fill = (book_edition.book_id, book_edition.edition_number, book_edition.isbn, book_edition.publisher, book_edition.publish_year, book_edition.number_of_pages, book_edition.language)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return book_edition.book_id, book_edition.edition_number

    def update(self, book_id, edition_number, book_edition):
        query = "UPDATE BOOK_EDITION SET ISBN = %s, PUBLISHER = %s, PUBLISH_YEAR = %s, NUMBER_OF_PAGES = %s, LANGUAGE = %s WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_edition.isbn, book_edition.publisher, book_edition.publish_year, book_edition.number_of_pages, book_edition.language, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()
            
        return book_edition.book_id, book_edition.edition_number

    def delete(self, book_id, edition_number):
        query = "DELETE FROM BOOK_EDITION WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def get_row(self, book_id, edition_number):
        _book_edition = None

        query = "SELECT * FROM BOOK_EDITION WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            book_edition = cursor.fetchone()
            if book_edition is not None:
                _book_edition = BookEditionObj(book_edition[0], book_edition[1], book_edition[2], book_edition[3], book_edition[4], book_edition[5], book_edition[6])

        return _book_edition

    def get_rows_by_book(self, book_id):
        book_edition_table = []
        if type(book_id) == int:
            book_id = str(book_id)

        query = "SELECT * FROM BOOK_EDITION WHERE (BOOK_ID = %s)"
        fill = (book_id)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query %fill)
            for book_edition in cursor:
                book_edition_ = BookEditionObj(book_edition[0], book_edition[1], book_edition[2], book_edition[3], book_edition[4], book_edition[5], book_edition[6])
                book_edition_table.append(book_edition_)
            cursor.close()

        return book_edition_table

    def get_table(self):
        book_edition_table = []

        query = "SELECT * FROM BOOK_EDITION;"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for book_edition in cursor:
                book_edition_ = BookEditionObj(book_edition[0], book_edition[1], book_edition[2], book_edition[3], book_edition[4], book_edition[5], book_edition[6])
                book_edition_table.append(book_edition_)
            cursor.close()

        return book_edition_table
