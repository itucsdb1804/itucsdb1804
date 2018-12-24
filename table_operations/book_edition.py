import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import BookEditionObj


class BookEdition(baseClass):
    def __init__(self):
        super().__init__("BOOK_EDITION", BookEditionObj)
        self.columns = {"book_id": "BOOK_ID", "edition_number": "EDITION_NUMBER", "isbn": "ISBN", "publisher": "PUBLISHER", "publish_year": "PUBLISH_YEAR", "number_of_pages": "NUMBER_OF_PAGES", "language": "LANGUAGE"}

    def add(self, book_edition):
        query = "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        fill = (book_edition.book_id, book_edition.edition_number, book_edition.isbn, book_edition.publisher, book_edition.publish_year, book_edition.number_of_pages, book_edition.language)
        self.execute(query, fill)

        return book_edition.book_id, book_edition.edition_number

    def delete(self, book_id, edition_number):
        query = "DELETE FROM BOOK_EDITION WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)
        self.execute(query, fill)

    def get_row(self, book_id, edition_number):
        return super().get_row("*", ["BOOK_ID", "EDITION_NUMBER"], [book_id, edition_number])

    def get_rows_by_book(self, book_id):
        return super().get_row("*", ["BOOK_ID"], [book_id])
