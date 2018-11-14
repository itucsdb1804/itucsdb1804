from flask import Flask, render_template
from database import Database
from tables import Book

app = Flask(__name__)

db = Database()
bookdb = db.book
bookdb.add_book(Book("Enver", 2018, "tip1", 6053326045, 784, "Türkiye İş Bankası Kültür Yayınları"))
bookdb.add_book(Book("Hayvan Çiftliği", 2018, "tür2", 9750719387, 152, "Can Yayınları"))
bookdb.add_book(Book("Simyacı", 2018, "tür1", 9750726439, 184, "Can Yayınları"))
bookdb.add_book(Book("Göçüp Gidenler Koleksiyoncusu", 2018, "tür3", 6602026351, 168, "Doğan Kitap"))
bookdb.add_book(Book("Osmanlı Gerçekleri", 2018, "tür2", 6050827644, 288, "Timaş Yayınları"))

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/books")
def books_page():
    books = bookdb.get_books()
    return render_template("books.html", books=sorted(books))

if __name__ == "__main__":
	app.run()
