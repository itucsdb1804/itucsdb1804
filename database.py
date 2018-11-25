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



