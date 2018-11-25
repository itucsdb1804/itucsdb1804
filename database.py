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
        self.customer = self.Customer(url)
        self.person = self.Person(url)
        self.address = self.Address(url)
        #self.author = self.Author(url)
        #self.book_author = self.Book_Author(url)
        #self.category = self.Category(url)
        #self.book_category = self.Book_Category(url)

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




