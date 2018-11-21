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
        self.store = self.Store(url)
        self.comment = self.Comment(url)

    class Book:
        def __init__(self, url):
            self.url = url

        def add_book(self, book):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO BOOK (NAME, WRITINGYEAR, TYPE, ISBN, NUMBEROFPAGES, PUBLISHER) VALUES (%s, %s, %s, %s, %s, %s)",
                    (book.name, book.date, book.type, book.isbn, book.numberOfPage, book.publisher))
                cursor.close()

        def update_book(self, book_key, book):
            query = "UPDATE BOOK SET NAME = %s, WRITINGYEAR = %s, TYPE = %s, ISBN = %s, NUMBEROFPAGES = %s, PUBLISHER = %s WHERE (BOOK_ID = %s)"
            fill = (book.name, book.date, book.type, book.isbn, book.numberOfPage, book.publisher, book_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete_book(self, book_key):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM BOOK WHERE BOOK_ID = %s", (book_key,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def get_book(self, book_key):
            _book = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM BOOK WHERE BOOK_ID = %s", (book_key,))
                book = cursor.fetchone()
                if book is not None:
                    _book = Book(book[1], book[2], book[3], book[4], book[5], book[6])
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return _book

        def get_books(self):
            books = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM BOOK;")
                for book in cursor:
                    book_ = Book(book[1], book[2], book[3], book[4], book[5], book[6])
                    books.append((book[0], book_))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

            return books
        
    class Store:
        def __init__(self, url):
            self.url = url

        def add(self, store):
            query = "INSERT INTO STORE (NAME, PHONE, ADRESS_ID, EMAIL, WEBSITE, OPENEDDATE, EXPLANATION) VALUES (%s, %s, %s, %s, %s, %s, %s)"    
            fill = (store.name, store.phone, store.address_id, store.email, store.website, store.opened_date, store.explanation)
            
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, store_id, store):
            query = "UPDATE STORE SET NAME = %s, PHONE = %s, ADRESS_ID = %s, EMAIL = %s, WEBSITE = %s, OPENEDDATE = %s, EXPLANATION = %s WHERE (STORE_ID = %s)"
            fill = (store.name, store.phone, store.address_id, store.email, store.website, store.opened_date, store.explanation, store_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, store_key):
            query = "DELETE FROM STORE WHERE STORE_ID = %s"
            fill = (store_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, store_key):
            _store = None

            query = "SELECT * FROM STORE WHERE STORE_ID = %s"
            fill = (store_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                store = cursor.fetchone()
                if store is not None:
                    _store = Store(store[1], store[2], store[3], store[4], store[5], store[6], store[7])

            return _store

        def get_table(self):
            stores = []

            query = "SELECT * FROM STORE;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for store in cursor:
                    store_ = Store(store[1], store[2], store[3], store[4], store[5], store[6], store[7])
                    stores.append((store[0], store_))
                cursor.close()

            return stores

    class Comment:
        def __init__(self, url):
            self.url = url
            self.dbname = "COMMENT"

        def add(self, comment):
            query = "INSERT INTO COMMENT (CUSTOMER_ID, TITLE, EXPLANATION, UPDATETIME, POINTTOBOOK) VALUES (%s, %s, %s, %s, %s)"    
            fill = (comment.customer_id, comment.title, comment.explanation, comment.update_time, comment.point_to_book)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, comment_key, comment):
            query = "UPDATE COMMENT SET CUSTOMER_ID = %s, TITLE = %s, EXPLANATION = %s, UPDATETIME = %s, POINTTOBOOK = %s WHERE (COMMENT_ID = %s)"
            fill = (comment.customer_id, comment.title, comment.explanation, comment.update_time, comment.point_to_book, comment_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, comment_key):
            query = "DELETE FROM COMMENT WHERE COMMENT_ID = %s"
            fill = (comment_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, comment_key):
            _comment = None

            query = "SELECT * FROM COMMENT WHERE COMMENT_ID = %s"
            fill = (comment_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                comment = cursor.fetchone()
                if comment is not None:
                    _comment = Comment(comment[1], comment[2], comment[3], comment[4], comment[5])

            return _comment

        def get_table(self):
            comments = []

            query = "SELECT * FROM COMMENT;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for comment in cursor:
                    comment_ = Comment(comment[1], comment[2], comment[3], comment[4], comment[5])
                    comments.append((comment[0], comment_))
                cursor.close()

            return comments
