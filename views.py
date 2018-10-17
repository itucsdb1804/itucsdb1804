from flask import render_template


def home_page():
    return render_template("home.html")


def books_page():
    return render_template("books.html") 
