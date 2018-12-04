from flask import current_app, render_template, abort, request, redirect, url_for
import datetime
from tables import *


def home_page():
    return render_template("home.html")


def books_page():
    db = current_app.config["db"]
    if request.method == "GET":
        books = db.book.get_table()
        return render_template("books.html", books=sorted(books))
    else:
        form_book_keys = request.form.getlist("book_keys")
        for form_book_key in form_book_keys:
            print("My output:", form_book_key, type(form_book_key))
            db.book.delete(form_book_key)
        return redirect(url_for("books_page"))


def book_page(book_key):
    db = current_app.config["db"]
    book = db.book.get_row(book_key)
    editions = db.book_edition.get_rows_by_book(book_key)
    if book is None:
        abort(404)
    return render_template("book.html", book=book, book_key=book_key, editions=editions)


def book_add_page():
    db = current_app.config["db"]
    if request.method == "GET":
        values = {"book_name": "", "released_year": "", "explanation": ""}
        return render_template("forms/book_edit.html", min_year=1887, max_year=datetime.datetime.now().year, values=values)
    else:
        form_name = request.form["book_name"]
        form_year = request.form["released_year"]
        form_explanation = request.form["explanation"]
        book = Book(form_name, form_year, form_explanation)
        #
        # book_key = db.book.add_book(book)
        # return redirect(url_for("book_page", book_key=book_key))
        db.book.add_book(book)
        return redirect(url_for("books_page"))


def book_edit_page(book_key):
    db = current_app.config["db"]
    if request.method == "GET":
        book = db.book.get_row(book_key)
        if book is None:
            abort(404)
        values = {"book_name": book.book_name, "released_year": book.release_year, "explanation": book.explanation }
        return render_template("forms/book_edit.html", min_year=1887, max_year=datetime.datetime.now().year, values=values)
    else:
        form_name = request.form["book_name"]
        form_year = request.form["released_year"]
        form_explanation = request.form["explanation"]
        book = Book(form_name, form_year, form_explanation)
        db.book.update(book_key, book)
        return redirect(url_for("book_page", book_key=book_key))


def book_delete_page(book_key):
    db = current_app.config["db"]
    db.book.delete(book_key)
    return redirect(url_for("books_page"))


def stores_page():
    db = current_app.config["db"]
    stores = db.store.get_table()
    return render_template("stores.html", stores=sorted(stores))


def comments_page():
    db = current_app.config["db"]
    comments = db.comment.get_table()
    return render_template("comments.html", comments=sorted(comments))


def customers_page():
    db = current_app.config["db"]
    customers = db.customer.get_table()
    return render_template("customers.html", customers=customers)


def addresses_page():
    db = current_app.config["db"]
    addresses = db.address.get_table()
    return render_template("addresses.html", addresses=addresses)


def persons_page():
    db = current_app.config["db"]
    persons = db.person.get_table()
    return render_template("persons.html", persons=persons)
#
#
# def person_add_page():
#     db = current_app.config["db"]
#     if request.method == "GET":
#         values = {"name": "", "surname": "", "gender": "", "date_of_birth": "", "nationality": ""}
#         return render_template("forms/person_edit.html", values=values)
#     else:
#         p_name = request.form["name"]
#         p_surname = request.form["surname"]
#         p_gender = request.form["gender"]
#         p_date_of_birth = request.form["date_of_birth"]
#         p_nationality = request.form["nationality"]
#
#         print(p_name, p_surname, p_gender, p_date_of_birth, p_nationality)
#
#         return redirect(url_for("persons_page"))
#
#
# def person_edit_page(person_key):
#     db = current_app.config["db"]
#     if request.method == "GET":
#         person = db.book.get_row(book_key)
#         if book is None:
#             abort(404)
#         values = {"book_name": book.book_name, "released_year": book.release_year, "explanation": book.explanation }
#         return render_template("forms/book_edit.html", min_year=1887, max_year=datetime.datetime.now().year, values=values)
#     else:
#         form_name = request.form["book_name"]
#         form_year = request.form["released_year"]
#         form_explanation = request.form["explanation"]
#         book = Book(form_name, form_year, form_explanation)
#         db.book.update(book_key, book)
#         return redirect(url_for("book_page", book_key=book_key))


def login_page():
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template("login.html")
    else:
        user_name = request.form["inputUsername"]
        user_password = request.form["inputPassword"]

        # Login operations

        return redirect(url_for("home_page"))


def signup_page():
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template("signup.html")


def products_page():
    db = current_app.config["db"]
    if request.method == "GET":
        tables = db.product.get_products_all_info()
        return render_template("products.html", tables=tables)
    else:
        return redirect(url_for("products_page"))


def book_edition_page(book_id, edition_number):
    db = current_app.config["db"]
    book_edition = db.book_edition.get_row(book_id, edition_number)
    if book_edition is None:
        abort(404)
    return render_template("book_edition.html", book_id=book_id, edition_number=edition_number, book_edition=book_edition)


def book_edition_add_page():
    db = current_app.config["db"]
    if request.method == "GET":
        values = {"book_id": "", "edition_number": "", "isbn": "", "publisher": "", "publish_year": "", "number_of_pages": "", "language": ""}
        books = db.book.get_table()
        for j, i in books:
            print(i.book_name, i.book_id)
        return render_template("forms/book_edition_edit.html", values=values, title="Book Edition Adding", books=books)
    else:
        book_edition = BookEdition(request.form["book_id"], request.form["edition_number"], request.form["isbn"], request.form["publisher"], request.form["publish_year"], request.form["number_of_pages"], request.form["language"])
        book_id, edition_number = db.book_edition.add(book_edition)
        return redirect(url_for("book_edition_page", book_id=book_id, edition_number=edition_number))


def book_edition_edit_page(book_id, edition_number):
    db = current_app.config["db"]
    if request.method == "GET":
        book_edition = db.book_edition.get_row(book_id, edition_number)
        if book_edition is None:
            abort(404)
        values = {"book_id": book_edition.book_id, "edition_number": book_edition.edition_number, "isbn": book_edition.isbn, "publisher": book_edition.publisher, "publish_year": book_edition.publish_year, "number_of_pages": book_edition.number_of_pages, "language": book_edition.language}
        books = db.book.get_table()
        return render_template("forms/book_edition_edit.html", values=values, title="Book Edition Adding", books=books)
    else:
        book_edition = BookEdition(request.form["book_id"], request.form["edition_number"], request.form["isbn"], request.form["publisher"], request.form["publish_year"], request.form["number_of_pages"], request.form["language"])
        book_id, edition_number = db.book_edition.update(book_id, edition_number, book_edition)
        return redirect(url_for("book_edition_page", book_id=book_id, edition_number=edition_number))


def book_edition_delete_page(book_id, edition_number):
    db = current_app.config["db"]
    db.book_edition.delete(book_id, edition_number)
    return redirect(url_for("book_page", book_key=book_id))

