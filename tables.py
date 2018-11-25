# myilmaz
class Book:
    def __init__(self, book_name, release_year, explanation):
        self.book_name = book_name
        self.release_year = release_year
        self.explanation = explanation


class Category:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name


class Book_Category:
    def __init__(self, book_id, category_id):
        self.book_id = book_id
        self.category_id = category_id


class Person:
    def __init__(self, person_id, person_name, surname, gender, date_of_birth, nationality):
        self.person_id = person_id
        self.person_name = person_name
        self.surname = surname
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.nationality = nationality


class Customer:
    def __init__(self, customer_id, person_id, username, email, password_hash, phone, is_active):
        self.customer_id = customer_id
        self.person_id = person_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
        self.is_active = is_active


class Address:
    def __init__(self, address_id, address_name, country, city, district, neighborhood, avenue, street, addr_number, zipcode, explanation):
        self.address_id = address_id
        self.address_name = address_name
        self.country = country
        self.city = city
        self.district = district
        self.neighborhood = neighborhood
        self.avenue = avenue
        self.street = street
        self.addr_number = addr_number
        self.zipcode = zipcode
        self.explanation = explanation


class Author:
    def __init__(self, author_id, person_id, biography):
        self.author_id = author_id
        self.person_id = person_id
        self.biography = biography


class Book_Author:
    def __init__(self, book_id, author_id):
        self.book_id = book_id
        self.author_id = author_id


# myilmaz
class Store:
    def __init__(self, store_name, store_phone, address_id, email, website, date_added, explanation):
        self.store_name = store_name
        self.store_phone = store_phone
        self.address_id = address_id
        self.email = email
        self.website = website
        self.date_added = date_added
        self.explanation = explanation


# myilmaz
class Comment:
    def __init__(self, customer_id, book_id, comment_title, comment_statement, added_time, updated_time, rating):
        self.customer_id = customer_id
        self.book_id = book_id
        self.comment_title = comment_title
        self.comment_statement = comment_statement
        self.added_time = added_time
        self.updated_time = updated_time
        self.rating = rating


# myilmaz
class CustomerAddress:
    def __init__(self, customer_id, address_id):
        self.customer_id = customer_id
        self.address_id = address_id


# myilmaz
class BookEdition:
    def __init__(self, book_id, edition_number, isbn, publisher, publish_year, number_of_pages, language):
        self.book_id = book_id
        self.edition_number = edition_number
        self.isbn = isbn
        self.publisher = publisher
        self.publish_year = publish_year
        self.number_of_pages = number_of_pages
        self.language = language


# myilmaz
class Transaction:
    def __init__(self, customer_id, address_id, transaction_time, payment_type, explanation):
        self.customer_id = customer_id
        self.address_id = address_id
        self.transaction_time = transaction_time
        self.payment_type = payment_type
        self.explanation = explanation


# myilmaz
class Product:
    def __init__(self, store_id, book_id, edition_number, remaining, actual_price, number_of_sells, date_added, explanation, is_active):
        self.store_id = store_id
        self.book_id = book_id
        self.edition_number = edition_number
        self.remaining = remaining
        self.actual_price = actual_price
        self.number_of_sells = number_of_sells
        self.date_added = date_added
        self.explanation = explanation
        self.is_active = is_active


# myilmaz
class TransactionProduct:
    def __init__(self, transaction_id, store_id, book_id, edition_number, piece, unit_price):
        self.transaction_id = transaction_id
        self.store_id = store_id
        self.book_id = book_id
        self.edition_number = edition_number
        self.piece = piece
        self.unit_price = unit_price