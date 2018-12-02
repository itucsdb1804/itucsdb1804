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
        self.category = self.Category(url)
        self.book_category = self.Book_Category(url)
        self.person = self.Person(url)
        self.customer = self.Customer(url)
        self.address = self.Address(url)
        self.author = self.Author(url)
        self.book_author = self.Book_Author(url)
        self.store = self.Store(url)
        self.comment = self.Comment(url)
        self.customer_address = self.CustomerAddress(url)
        self.book_edition = self.BookEdition(url)
        self.transaction = self.Transaction(url)
        self.product = self.Product(url)
        self.transaction_product = self.TransactionProduct(url)

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
            if type(book_key) == int:
                book_key = str(book_key)

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

    class Category:
        def __init__(self, url):
            self.url = url
            self.dbname = "CATEGORY"

        def add(self, category):
            query = "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES (%s)"    
            fill = (category.category_name)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, category):
            query = "UPDATE CATEGORY SET CATEGORY_NAME = %s WHERE (CATEGORY_ID = %s)"
            fill = (category.category_name, category.category_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, category):
            query = "DELETE FROM CATEGORY WHERE CATEGORY_ID = %s"
            fill = (category.category_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, cat_id):
            _category = None

            query = "SELECT * FROM CATEGORY WHERE CATEGORY_ID = %s"
            fill = (cat_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                category = cursor.fetchone()
                if category is not None:
                    _category = Category(category[0], category[1])

            return _category

        def get_table(self):
            categories = []

            query = "SELECT * FROM CATEGORY;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for category in cursor:
                    category_ = Category(category[0], category[1])
                    categories.append(category_)
                cursor.close()

            return categories

    class Book_Category:
        def __init__(self, url):
            self.url = url
            self.dbname = "BOOK_CATEGORY"

        def add(self, book_category):
            query = "INSERT INTO BOOK_CATEGORY (BOOK_ID, CATEGORY_ID) VALUES (%s, %s)"    
            fill = (book_category.book_id, book_category.category_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, book_category):    # Searches by book_id, update category_id
    
            query = "UPDATE BOOK_CATEGORY SET CATEGORY_ID = %s WHERE (BOOK_ID = %s)"
            fill = (book_category.category_id, book_category.book_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, book_category):
            query = "DELETE FROM BOOK_CATEGORY WHERE ((BOOK_ID = %s) AND (CATEGORY_ID = %s))"
            fill = (book_category.book_id, book_category.category_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, id_val, search_by_book_id):
            attr = "BOOK_ID" if search_by_book_id else "CATEGORY_ID"
            _book_category = None

            query = "SELECT * FROM BOOK_CATEGORY WHERE (%s = %s)"
            fill = (attr, id_val)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                book_category = cursor.fetchone()
                if book_category is not None:
                    _book_category = Book_Category(book_category[0], book_category[1])

            return _book_category

        def get_table(self):
            book_categories = []

            query = "SELECT * FROM BOOK_CATEGORY;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for book_category in cursor:
                    book_category_ = Book_Category(book_category[0], book_category[1])
                    book_categories.append(book_category_)
                cursor.close()

            return book_categories

    class Person:
        def __init__(self, url):
            self.url = url
            self.dbname = "PERSON"

        def add(self, person):
            query = "INSERT INTO PERSON (PERSON_NAME, SURNAME, GENDER, DATE_OF_BIRTH, NATIONALITY) VALUES (%s, %s, %s, %s, %s)"    
            fill = (person.person_name, person.surname, person.gender, person.date_of_birth, person.nationality)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, person):
            query = "UPDATE PERSON SET PERSON_NAME = %s, SURNAME = %s, GENDER = %s, DATE_OF_BIRTH = %s, NATIONALITY = %s WHERE (PERSON_ID = %s)"
            fill = (person.person_name, person.surname, person.gender, person.date_of_birth, person.nationality, person.person_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, person):
            query = "DELETE FROM PERSON WHERE PERSON_ID = %s"
            fill = (person.person_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, pers_id):
            _person = None

            query = "SELECT * FROM PERSON WHERE PERSON_ID = %s"
            fill = (pers_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                person = cursor.fetchone()
                if person is not None:
                    _person = Person(person[0], person[1], person[2], person[3], person[4], person[5])

            return _person

        def get_table(self):
            people = []

            query = "SELECT * FROM PERSON;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for person in cursor:
                    person_ = Person(person[0], person[1], person[2], person[3], person[4], person[5])
                    people.append(person_)
                cursor.close()

            return people

    class Customer:
        def __init__(self, url):
            self.url = url
            self.dbname = "CUSTOMER"

        def add(self, customer):
            query = "INSERT INTO CUSTOMER (PERSON_ID, USERNAME, EMAIL, PASS_HASH, PHONE, IS_ACTIVE) VALUES (%s, %s, %s, %s, %s, %s)"    
            fill = (customer.person_id, customer.username, customer.email, customer.pass_hash, customer.phone, customer.is_active)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, customer):
            query = "UPDATE CUSTOMER SET USERNAME = %s, EMAIL = %s, PASS_HASH = %s, PHONE = %s, IS_ACTIVE = %s WHERE (CUSTOMER_ID = %s)"
            fill = (customer.username, customer.email, customer.pass_hash, customer.phone, customer.is_active, customer.customer_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, customer):
            query = "DELETE FROM CUSTOMER WHERE CUSTOMER_ID = %s"
            fill = (customer.customer_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, cust_id):
            _customer = None

            query = "SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = %s"
            fill = (cust_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                customer = cursor.fetchone()
                if customer is not None:
                    _customer = Customer(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6])

            return _customer

        def get_table(self):
            customers = []

            query = "SELECT * FROM CUSTOMER;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for customer in cursor:
                    customer_ = Customer(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6])
                    customers.append(customer_)
                cursor.close()

            return customers

    class Address:
        def __init__(self, url):
            self.url = url
            self.dbname = "ADDRESS"

        def add(self, address):
            query = "INSERT INTO ADDRESS (ADDRESS_NAME, COUNTRY, CITY, DISTRICT, NEIGHBORHOOD, AVENUE, STREET, ADDR_NUMBER, ZIPCODE, EXPLANATION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"    
            fill = (address.address_name, address.country, address.city, address.district, address.neighborhood, address.avenue, address.street, address.addr_number, address.zipcode, address.explanation)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, address):
            query = "UPDATE ADDRESS SET ADDRESS_NAME = %s, COUNTRY = %s, CITY = %s, DISTRICT = %s, NEIGHBORHOOD = %s, AVENUE = %s, STREET = %s, ADDR_NUMBER = %s, ZIPCODE = %s, EXPLANATION = %s WHERE (ADDRESS_ID = %s)"
            fill = (address.address_name, address.country, address.city, address.district, address.neighborhood, address.avenue, address.street, address.addr_number, address.zipcode, address.explanation, address.address_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, address):
            query = "DELETE FROM ADDRESS WHERE ADDRESS_ID = %s"
            fill = (address.address_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, addr_id):
            _address = None

            query = "SELECT * FROM ADDRESS WHERE ADDRESS_ID = %s"
            fill = (addr_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                address = cursor.fetchone()
                if address is not None:
                    _address = Address(address[0], address[1], address[2], address[3], address[4], address[5], address[6], address[7], address[8], address[9], address[10])

            return _address

        def get_table(self):
            addresses = []

            query = "SELECT * FROM ADDRESS;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for address in cursor:
                    address_ = Address(address[0], address[1], address[2], address[3], address[4], address[5], address[6], address[7], address[8], address[9], address[10])
                    addresses.append(address_)
                cursor.close()

            return addresses

    class Author:
        def __init__(self, url):
            self.url = url
            self.dbname = "AUTHOR"

        def add(self, author):
            query = "INSERT INTO AUTHOR (PERSON_ID, BIOGRAPHY) VALUES (%s, %s)"    
            fill = (author.person_id, author.biography)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, author):
            query = "UPDATE AUTHOR SET PERSON_ID = %s, BIOGRAPHY = %s WHERE (AUTHOR_ID = %s)"
            fill = (author.person_id, author.biography, author.author_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, author):
            query = "DELETE FROM AUTHOR WHERE AUTHOR_ID = %s"
            fill = (author.author_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, aut_id):
            _author = None

            query = "SELECT * FROM AUTHOR WHERE AUTHOR_ID = %s"
            fill = (aut_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                author = cursor.fetchone()
                if author is not None:
                    _author = Author(author[0], author[1], author[2])

            return _author

        def get_table(self):
            authors = []

            query = "SELECT * FROM AUTHOR;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for author in cursor:
                    author_ = Author(author[0], author[1], author[2])
                    authors.append(author_)
                cursor.close()

            return authors

    class Book_Author:
        def __init__(self, url):
            self.url = url
            self.dbname = "BOOK_AUTHOR"

        def add(self, book_author):
            query = "INSERT INTO BOOK_AUTHOR (BOOK_ID, AUTHOR_ID) VALUES (%s, %s)"    
            fill = (book_author.book_id, book_author.author_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, book_author, update_book_id):  #if update_book_id=True, then searchs for author_id
            first_attr = "BOOK_ID" if update_book_id else "AUTHOR_ID"
            second_attr = "AUTHOR_ID" if update_book_id else "BOOK_ID"
            first_val = book_author.book_id if update_book_id else book_author.author_id
            second_val = book_author.author_id if update_book_id else book_author.book_id
    
            query = "UPDATE BOOK_AUTHOR SET %s = %s WHERE (%s = %s)"
            fill = (first_attr, first_val, second_attr, second_val)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, book_author):
            query = "DELETE FROM BOOK_AUTHOR WHERE ((BOOK_ID = %s) AND (AUTHOR_ID = %s))"
            fill = (book_author.book_id, book_author.author_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, id_val, search_by_book_id):
            attr = "BOOK_ID" if search_by_book_id else "AUTHOR_ID"
            _book_author = None

            query = "SELECT * FROM BOOK_AUTHOR WHERE (%s = %s)"
            fill = (attr, id_val)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                book_author = cursor.fetchone()
                if book_author is not None:
                    _book_author = Book_Author(book_author[0], book_author[1])

            return _book_author

        def get_table(self):
            book_authors = []

            query = "SELECT * FROM BOOK_AUTHOR;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for book_author in cursor:
                    book_author_ = Book_Author(book_author[0], book_author[1])
                    book_authors.append(book_author_)
                cursor.close()

            return book_authors

    # myilmaz
    class Store:
        def __init__(self, url):
            self.url = url

        def add(self, store):
            query = "INSERT INTO STORE (STORE_NAME, STORE_PHONE, ADDRESS_ID, EMAIL, WEBSITE, DATE_ADDED, EXPLANATION) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            fill = (store.store_name, store.store_phone, store.address_id, store.email, store.website, store.date_added, store.explanation)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, store_key, store):
            query = "UPDATE BOOK SET STORE_NAME = %s, STORE_PHONE = %s, ADDRESS_ID = %s, EMAIL = %s, WEBSITE = %s, DATE_ADDED = %s, EXPLANATION = %s WHERE STORE_ID = %s"
            fill = (store.store_name, store.store_phone, store.address_id, store.email, store.website, store.date_added, store.explanation, store_key)

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

    # myilmaz
    class Comment:
        def __init__(self, url):
            self.url = url

        def add(self, comment):
            query = "INSERT INTO COMMENT (CUSTOMER_ID, BOOK_ID, COMMENT_TITLE, COMMENT_STATEMENT, ADDED_TIME, UPDATED_TIME, RATING) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            fill = (comment.customer_id, comment.book_id, comment.comment_title, comment.comment_statement, comment.added_time, comment.updated_time, comment.rating)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, comment_key, comment):
            query = "UPDATE COMMENT SET CUSTOMER_ID = %s, BOOK_ID = %s, COMMENT_TITLE = %s, COMMENT_STATEMENT = %s, ADDED_TIME = %s, UPDATED_TIME = %s, RATING = %s WHERE COMMENT_ID = %s"
            fill = (comment.customer_id, comment.book_id, comment.comment_title, comment.comment_statement, comment.added_time, comment.updated_time, comment.rating, comment_key)

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
                    _comment = Comment(comment[1], comment[2], comment[3], comment[4], comment[5], comment[6], comment[7])

            return _comment

        def get_table(self):
            comments = []

            query = "SELECT * FROM COMMENT;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for comment in cursor:
                    comment_ = Comment(comment[1], comment[2], comment[3], comment[4], comment[5], comment[6], comment[7])
                    comments.append((comment[0], comment_))
                cursor.close()

            return comments

    # myilmaz
    class CustomerAddress:
        def __init__(self, url):
            self.url = url

        def add(self, customer_address):
            query = "INSERT INTO CUSTOMER_ADDRESS (CUSTOMER_ID, ADDRESS_ID) VALUES (%s, %s)"
            fill = (customer_address.customer_id, customer_address.address_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, old_customer_address, updated_customer_address):  # Update address id by customer_id and adress_id

            query = "UPDATE CUSTOMER_ADDRESS SET ADDRESS_ID = %s ((CUSTOMER_ID = %s) AND (ADDRESS_ID = %s))"
            fill = (updated_customer_address.address_id, old_customer_address.customer_id, old_customer_address.address_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        # TODO delete all address of a customer, using "customer_address.address_id = none"
        def delete(self, customer_address):
            query = "DELETE FROM CUSTOMER_ADDRESS WHERE ((CUSTOMER_ID = %s) AND (ADDRESS_ID = %s))"
            fill = (customer_address.customer_id, customer_address.address_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        # TODO None olmayanlara göre seçme yap
        def get_address_ids_by_customer_id(self, customer_id):
            _address_ids = []

            # TODO acaba "SELECT ADDRESS_ID" olur mu?
            query = "SELECT * FROM CUSTOMER_ADDRESS WHERE (CUSTOMER_ID = %s)"
            fill = (customer_id)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                for customer_address in cursor:
                    _address_ids.append(customer_address[1])

            return _address_ids

        def get_table(self):
            customer_addresses = []

            query = "SELECT * FROM CUSTOMER_ADDRESS;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for customer_address in cursor:
                    customer_address_ = CustomerAddress(customer_address[0], customer_address[1])
                    customer_address.append(customer_address_)
                cursor.close()

            return customer_addresses

    # myilmaz
    class BookEdition:
        def __init__(self, url):
            self.url = url

        def add(self, book_edition):
            query = "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            fill = (book_edition.book_id, book_edition.edition_number, book_edition.isbn, book_edition.publisher, book_edition.publish_year, book_edition.number_of_pages, book_edition.language)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, book_id, edition_number, book_edition):
            query = "UPDATE BOOK_EDITION SET ISBN = %s, PUBLISHER = %s, PUBLISH_YEAR = %s, NUMBER_OF_PAGES = %s, LANGUAGE = %s WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
            fill = (book_edition.isbn, book_edition.publisher, book_edition.publish_year, book_edition.number_of_pages, book_edition.language, book_id, edition_number)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

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
                    _book_edition = BookEdition(book_edition[0], book_edition[1], book_edition[2], book_edition[3], book_edition[4], book_edition[5], book_edition[6])

            return _book_edition

        def get_table(self):
            book_edition_table = []

            query = "SELECT * FROM BOOK_EDITION;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for book_edition in cursor:
                    book_edition_ = BookEdition(book_edition[0], book_edition[1], book_edition[2], book_edition[3], book_edition[4], book_edition[5], book_edition[6])
                    book_edition_table.append(book_edition_)
                cursor.close()

            return book_edition_table

    # myilmaz
    class Transaction:
        def __init__(self, url):
            self.url = url

        def add(self, transaction):
            query = "INSERT INTO TRANSACTION (CUSTOMER_ID, ADDRESS_ID, TRANSACTION_TIME, PAYMENT_TYPE, EXPLANATION) VALUES (%s, %s, %s, %s, %s)"
            fill = (transaction.customer_id, transaction.address_id, transaction.transaction_time, transaction.payment_type, transaction.explanation)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, transaction_key, transaction):
            query = "UPDATE TRANSACTION SET CUSTOMER_ID = %s, ADDRESS_ID = %s, TRANSACTION_TIME = %s, PAYMENT_TYPE = %s, EXPLANATION = %s WHERE TRANSACTION_ID = %s"
            fill = (transaction.customer_id, transaction.address_id, transaction.transaction_time, transaction.payment_type, transaction.explanation, transaction_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, transaction_key):
            query = "DELETE FROM TRANSACTION WHERE TRANSACTION_ID = %s"
            fill = (transaction_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, transaction_key):
            _transaction = None

            query = "SELECT * FROM TRANSACTION WHERE TRANSACTION_ID = %s"
            fill = (transaction_key)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                transaction = cursor.fetchone()
                if transaction is not None:
                    _transaction = Transaction(transaction[1], transaction[2], transaction[3], transaction[4], transaction[5])

            return _transaction

        def get_table(self):
            transactions = []

            query = "SELECT * FROM TRANSACTION;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for transaction in cursor:
                    transaction_ = Transaction(transaction[1], transaction[2], transaction[3], transaction[4], transaction[5])
                    transactions.append((transaction[0], transaction_))
                cursor.close()

            return transactions

    # myilmaz
    class Product:
        def __init__(self, url):
            self.url = url

        def add(self, product):
            query = "INSERT INTO PRODUCT (STORE_ID, BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, DATE_ADDED, EXPLANATION, IS_ACTIVE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            fill = (product.store_id, product.book_id, product.edition_number, product.remaining, product.actual_price, product.number_of_sells, product.date_added, product.explanation, product.is_active)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, store_id, book_id, edition_number, product):
            query = "UPDATE PRODUCT SET REMAINING = %s, ACTUAL_PRICE = %s, NUMBER_OF_SELLS = %s, DATE_ADDED = %s, EXPLANATION = %s, IS_ACTIVE = %s WHERE ((STORE_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
            fill = (product.remaining, product.actual_price, product.number_of_sells, product.date_added, product.explanation, product.is_active, store_id, book_id, edition_number)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, store_id, book_id, edition_number):
            query = "DELETE FROM PRODUCT WHERE ((STORE_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
            fill = (store_id, book_id, edition_number)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, store_id, book_id, edition_number):
            _product = None

            query = "SELECT * FROM PRODUCT WHERE ((STORE_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
            fill = (store_id, book_id, edition_number)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                product = cursor.fetchone()
                if product is not None:
                    _product = Product(product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8])

            return _product

        def get_table(self):
            products = []

            query = "SELECT * FROM BOOK_EDITION;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for product in cursor:
                    product_ = Product(product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8])
                    products.append(product_)
                cursor.close()

            return products

    # myilmaz
    class TransactionProduct:
        def __init__(self, url):
            self.url = url

        def add(self, transaction_product):
            query = "INSERT INTO TRANSACTION_PRODUCT (TRANSACTION_ID, STORE_ID, BOOK_ID, EDITION_NUMBER, PIECE, UNIT_PRICE) VALUES (%s, %s, %s, %s, %s, %s)"
            fill = (transaction_product.transaction_id, transaction_product.store_id, transaction_product.book_id, transaction_product.edition_number, transaction_product.piece, transaction_product.unit_price)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def update(self, transaction_id, store_id, book_id, edition_number, transaction_product):
            query = "UPDATE TRANSACTION_PRODUCT SET PIECE = %s, UNIT_PRICE = %s WHERE ((TRANSACTION_ID = %s) AND (STORE_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
            fill = (transaction_product.piece, transaction_product.unit_price, transaction_id, store_id, book_id, edition_number)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def delete(self, transaction_id, store_id, book_id, edition_number):
            query = "DELETE FROM TRANSACTION_PRODUCT WHERE ((TRANSACTION_ID = %s) AND (STORE_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
            fill = (transaction_id, store_id, book_id, edition_number)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                cursor.close()

        def get_row(self, transaction_id, store_id, book_id, edition_number):
            _transaction_product = None

            query = "SELECT * FROM TRANSACTION_PRODUCT WHERE ((TRANSACTION_ID = %s) AND (STORE_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
            fill = (transaction_id, store_id, book_id, edition_number)

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query, fill)
                transaction_product = cursor.fetchone()
                if transaction_product is not None:
                    _transaction_product = TransactionProduct(transaction_product[0], transaction_product[1], transaction_product[2], transaction_product[3], transaction_product[4], transaction_product[5])

            return _transaction_product

        def get_table(self):
            transaction_product_table = []

            query = "SELECT * FROM BOOK_EDITION;"

            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                for transaction_product in cursor:
                    transaction_product_ = TransactionProduct(transaction_product[0], transaction_product[1], transaction_product[2], transaction_product[3], transaction_product[4], transaction_product[5])
                    transaction_product_table.append(transaction_product_)
                cursor.close()

            return transaction_product_table
