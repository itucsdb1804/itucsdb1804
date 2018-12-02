from flask import render_template
from database import Database
import datetime

db = Database()


def home_page():
    return render_template("home.html")


def books_page():
    books = db.book.get_table()
    return render_template("books.html", books=sorted(books))


def stores_page():
    stores = db.store.get_table()
    return render_template("stores.html", stores=sorted(stores))


def comments_page():
    comments = db.comment.get_table()
    return render_template("comments.html", comments=sorted(comments))


def customers_page():
    customers = db.customer.get_table()
    return render_template("customers.html", customers=customers)


def addresses_page():
    addresses = db.address.get_table()
    return render_template("addresses.html", addresses=addresses)


def persons_page():
    persons = db.person.get_table()
    return render_template("persons.html", persons=persons)


def movie_add_page():
    return render_template("edits/book_edit.html", min_year=1887, max_year=datetime.datetime.now().year)