from flask import Flask, render_template
from database import Database
from tables import *
import datetime

app = Flask(__name__)

db = Database()
db.book.add_book(Book("book name 1", 2011, "Explanation 1"))
db.book.add_book(Book("book name 2", 2011, "Explanation 2"))


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/books")
def books_page():
    books = db.book.get_table()
    return render_template("books.html", books=sorted(books))
    

if __name__ == "__main__":
    app.run()
