from table_operations.baseClass import baseClass
from tables import BookObj
import psycopg2 as dbapi2


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
                _book = BookObj(book[1], book[2], book[3], book_id=book[0])

        return _book

    def get_table(self, with_author=False, with_category=False):
        books = []

        query = "SELECT * FROM BOOK;"
        query_authors = "SELECT PERSON.PERSON_NAME, PERSON.SURNAME " \
                 "FROM BOOK_AUTHOR, AUTHOR, PERSON " \
                 "WHERE ( " \
                     "( " \
                         "(BOOK_AUTHOR.AUTHOR_ID = AUTHOR.AUTHOR_ID) AND " \
                         "(AUTHOR.PERSON_ID = PERSON.PERSON_ID) " \
                     ") AND " \
                     "((BOOK_AUTHOR.BOOK_ID = %s)) " \
                 ")"
        query_categories = "SELECT CATEGORY.CATEGORY_NAME FROM BOOK_CATEGORY, CATEGORY WHERE BOOK_CATEGORY.CATEGORY_ID = CATEGORY.CATEGORY_ID AND BOOK_CATEGORY.BOOK_ID = %s"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for book in cursor:
                ret_list = []
                book_ = BookObj(book[1], book[2], book[3], book_id=book[0])
                if not with_author and not with_category:
                    books.append(book_)
                else:
                    ret_list.append(book_)
                    if with_author:
                        author_names = []  # Kitabın bütün yazarlarını alma fonksiyonu
                        with connection.cursor() as curs:
                            try:
                                curs.execute(query_authors, (book_.book_id,))
                                for author in curs:
                                    author_names.append(author[0] + " " + author[1])
                                ret_list.append(author_names)
                            except dbapi2.Error as err:
                                print("Error: %s", err)
                    if with_category:
                        category_names = []
                        with connection.cursor() as curs:
                            try:
                                curs.execute(query_categories, (book_.book_id,))
                                for category_name in curs:
                                    category_names.append(category_name[0])
                                ret_list.append(category_names)
                            except dbapi2.Error as err:
                                print("Error: %s", err)

                    books.append(ret_list)
            cursor.close()

        return books
