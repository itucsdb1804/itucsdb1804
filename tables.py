class Book:
    def __init__(self, name, date, intype, isbn, numberOfPage, publisher):
        self.name = name
        self.date = date
        self.type = intype
        self.isbn = isbn
        self.numberOfPage = numberOfPage
        self.publisher = publisher

class Store:
	def __init__(self, name, phone, address_id, email, opened_date, explanation):
		self.name = name
		self.phone = phone
		self.address_id = address_id
		self.email = email
		self.opened_date = opened_date
		self.explanation = explanation

class Comment:
    def __init__(self, customer_id, title, explanation, update_time, point_to_book, publisher):
        self.customer_id = customer_id
        self.title = title
        self.explanation = explanation
        self.update_time = update_time
        self.point_to_book = point_to_book
        self.publisher = publisher
