from flask import Flask, render_template
from database import Database
from tables import *
import datetime

app = Flask(__name__)

db = Database()


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/books")
def books_page():
    books = db.book.get_table()
    return render_template("books.html", books=sorted(books))


@app.route("/stores")
def stores_page():
    stores = db.store.get_table()
    return render_template("stores.html", stores=sorted(stores))


@app.route("/comments")
def comments_page():
    comments = db.comment.get_table()
    return render_template("comments.html", comments=sorted(comments))


@app.route("/customers")
def customers_page():
    customers = db.customer.get_table()
    return render_template("customers.html", customers=customers)


@app.route("/addresses")
def addresses_page():
    addresses = db.address.get_table()
    return render_template("addresses.html", addresses=addresses)


@app.route("/persons")
def persons_page():
    persons = db.person.get_table()
    return render_template("persons.html", persons=persons)


if __name__ == "__main__":
    app.run()
