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