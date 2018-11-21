from flask import Flask, render_template
from database import Database
from tables import *
import datetime

app = Flask(__name__)

db = Database()
bookdb = db.book
bookdb.add_book(Book("Enver", 2018, "tip1", 6053326045, 784, "Türkiye İş Bankası Kültür Yayınları"))
bookdb.add_book(Book("Hayvan Çiftliği", 2018, "tür2", 9750719387, 152, "Can Yayınları"))
bookdb.add_book(Book("Simyacı", 2018, "tür1", 9750726439, 184, "Can Yayınları"))
bookdb.add_book(Book("Göçüp Gidenler Koleksiyoncusu", 2018, "tür3", 6602026351, 168, "Doğan Kitap"))
bookdb.add_book(Book("Osmanlı Gerçekleri", 2018, "tür2", 6050827644, 288, "Timaş Yayınları"))
db.store.add(Store("Store name 1", "+901234567899", 1, "email1@gmail.com", "website1.com", datetime.date(2005, 11, 18), "1 explanation explanation explanationex planationexp lanation "))
db.store.add(Store("Store name 2", "+904563348645", 2, "email2@gmail.com", "website2.com", datetime.date(2015, 1, 8), "2 explanation explanation explanationex planationexp lanation "))
db.comment.add(Comment(11, "Title 1", "Explanation 1", datetime.datetime.now(), 11))
db.comment.add(Comment(22, "Title 2", "Explanation 2", datetime.datetime.now(), 22))
    
@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/books")
def books_page():
    books = bookdb.get_books()
    return render_template("books.html", books=sorted(books))

@app.route("/stores")
def stores_page():
    stores = db.store.get_table()
    return render_template("stores.html", stores=sorted(stores))

@app.route("/comments")
def comments_page():
    comments = db.comment.get_table()
    return render_template("comments.html", comments=sorted(comments))

if __name__ == "__main__":
    app.run()
