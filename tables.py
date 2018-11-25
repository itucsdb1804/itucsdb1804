# myilmaz
class Book:
    def __init__(self, book_name, release_year, explanation):
        self.book_name = book_name
        self.release_year = release_year
        self.explanation = explanation


class Customer:
    def __init__(self, customer_id, person_id, username, email, password_hash, phone, is_active):
        self.customer_id = customer_id
        self.person_id = person_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
        self.is_active = is_active


class Person:
    def __init__(self, person_id, person_name, surname, gender, date_of_birth, nationality):
        self.person_id = person_id
        self.person_name = person_name
        self.surname = surname
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.nationality = nationality


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


