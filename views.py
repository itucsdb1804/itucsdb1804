from flask import current_app, render_template, abort, request, redirect, url_for, session, flash
import datetime
from tables import *
from table_operations.control import Control
from login import check_password, sign_up
from forms import LoginForm
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import login_user, logout_user, login_required


def home_page():
    return render_template("home.html")


def books_page():
    db = current_app.config["db"]
    if request.method == "GET":
        books = db.book.get_table(with_author=True)
        return render_template("books.html", books=books)
    else:
        form_book_keys = request.form.getlist("book_keys")
        for form_book_key in form_book_keys:
            print("My output:", form_book_key, type(form_book_key))
            db.book.delete(form_book_key)
        return redirect(url_for("books_page"))


def book_page(book_key):
    db = current_app.config["db"]

    # Take book information
    book = db.book.get_row(book_key)
    # If there is no book with this book_key, abort 404 page
    if book is None:
        abort(404)

    # Take editions, authors, and comments of this book
    editions = db.book_edition.get_rows_by_book(book_key)
    author_names = []  # TODO Kitabın bütün yazarlarını alma fonksiyonu
    for book_author in db.book_author.get_table(where_columns="BOOK_ID", where_values=book_key):
        for author in db.author.get_table(where_columns="AUTHOR_ID", where_values=book_author.author_id):
            for person in db.person.get_table(where_columns="PERSON_ID", where_values=author.person_id):
                author_names.append(person.person_name + " " + person.person_surname)
    comments = db.comment.get_table()  # TODO !!!Kitabın!!! bütün yorumlarını alma fonksiyonu

    # If the book page is displayed
    if request.method == "GET":
        # Blank comment form
        new_comment_values = {"customer_id": "", "book_id": "", "comment_title": "", "comment_statement": "", "rating": ""}
        return render_template("book.html", book=book, authors=author_names, editions=editions, comments=comments, new_comment_values=new_comment_values)
    # If the new comment is added
    else:
        # Take values from add_comment form
        # TODO take customer_id from login system
        new_comment_values = {"customer_id": 1, "book_id": book_key, "comment_title": request.form["comment_title"], "comment_statement": request.form["comment_statement"], "rating": request.form["rating"]}

        comment_err_message = Control().Input().comment(new_comment_values)
        if comment_err_message:
            return render_template("book.html", book=book, authors=author_names, editions=editions, comments=comments, comment_err_message=comment_err_message, new_comment_values=new_comment_values)

        # Add comment to database
        comment = CommentObj(new_comment_values["customer_id"], new_comment_values["book_id"], new_comment_values["comment_title"], new_comment_values["comment_statement"], new_comment_values["rating"])
        db.comment.add(comment)

        return redirect(url_for("book_page", book_key=book_key))


def book_add_page():
    db = current_app.config["db"]
    err_message = None
    # TODO Control - Get authors because of selecting book's authors
    authors = []
    for author in db.author.get_table():
        authors.append((author, db.person.get_row(where_columns="PERSON_ID", where_values=author.person_id)))

    if request.method == "GET":
        values = {"book_name": "", "released_year": "", "explanation": "", "selected_author_ids": ""}
        return render_template("forms/book_edit.html", min_year=1887, max_year=datetime.datetime.now().year, values=values, title="Book adding", err_message=err_message, authors=authors)
    else:
        values = {"book_name": request.form["book_name"], "released_year": request.form["released_year"], "explanation": request.form["explanation"], "selected_author_ids": request.form["selected_author_ids"]}

        # Invalid input control
        err_message = Control().Input().book(values)
        if err_message:
            return render_template("forms/book_edit.html", min_year=1887, max_year=datetime.datetime.now().year, values=values, title="Book adding", err_message=err_message, authors=authors)

        book = BookObj(values["book_name"], values["released_year"], values["explanation"])
        # TODO Control -  Get book_id last added book
        book_id = db.book.add_book(book)
        for author_id in values["selected_author_ids"]:
            db.book_author.add(book_id, author_id)
        return redirect(url_for("books_page"))


def book_edit_page(book_key):
    db = current_app.config["db"]
    err_message = None
    # TODO Control - Get authors because of selecting book's authors
    authors = []
    for author in db.author.get_table():
        authors.append((author, db.person.get_row(where_columns="PERSON_ID", where_values=author.person_id)))

    if request.method == "GET":
        book = db.book.get_row(book_key)
        if book is None:
            abort(404)
        # Get author ids of this book
        selected_author_ids = []
        for book_author in db.book_author.get_table(where_columns="BOOK_ID", where_values=book.book_id):
            selected_author_ids.append(book_author.author_id)
        values = {"book_name": book.book_name, "released_year": book.release_year, "explanation": book.explanation, "selected_author_ids": selected_author_ids}
        return render_template("forms/book_edit.html", min_year=1887, max_year=datetime.datetime.now().year, values=values, title="Book editing", err_message=err_message)
    else:
        values = {"book_name": request.form["book_name"], "released_year": request.form["released_year"],
                  "explanation": request.form["explanation"]}

        # Invalid input control
        err_message = Control().Input().book(values)
        if err_message:
            return render_template("forms/book_edit.html", min_year=1887, max_year=datetime.datetime.now().year, values=values, title="Book adding", err_message=err_message)

        book = BookObj(values["book_name"], values["released_year"], values["explanation"])
        book_id = db.book.update(book)
        db.book_author.delete(where_columns="BOOK_ID", where_values=book_id)
        for author_id in values["selected_author_ids"]:
            db.book_author.add(book_id, author_id)
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
    return render_template("comments.html", comments=comments)


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
    err_message = None
    books = db.book.get_table()
    if request.method == "GET":
        values = {"book_id": "", "edition_number": "", "isbn": "", "publisher": "", "publish_year": "", "number_of_pages": "", "language": ""}
        return render_template("forms/book_edition_edit.html", values=values, title="Book Edition Adding", books=books, err_message=err_message)
    else:
        values = {'book_id': request.form["book_id"], 'edition_number': request.form["edition_number"], 'isbn': request.form["isbn"], 'publisher': request.form["publisher"], 'publish_year': request.form["publish_year"], 'number_of_pages': request.form["number_of_pages"], 'language': request.form["language"]}
        err_message = Control().Input().book_edition(values)
        if err_message:
            return render_template("forms/book_edition_edit.html", values=values, title="Book Edition Adding", books=books, err_message=err_message)

        book_edition = BookEditionObj(values["book_id"], values["edition_number"], values["isbn"], values["publisher"], values["publish_year"], values["number_of_pages"], values["language"])
        book_id, edition_number = db.book_edition.add(book_edition)
        return redirect(url_for("book_edition_page", book_id=book_id, edition_number=edition_number))


def book_edition_edit_page(book_id, edition_number):
    db = current_app.config["db"]
    err_message = None
    books = db.book.get_table()
    if request.method == "GET":
        book_edition = db.book_edition.get_row(book_id, edition_number)
        if book_edition is None:
            abort(404)
        values = {"book_id": book_edition.book_id, "edition_number": book_edition.edition_number, "isbn": book_edition.isbn, "publisher": book_edition.publisher, "publish_year": book_edition.publish_year, "number_of_pages": book_edition.number_of_pages, "language": book_edition.language}
        return render_template("forms/book_edition_edit.html", values=values, title="Book Edition Adding", books=books, err_message=err_message)
    else:
        values = {'book_id': request.form["book_id"], 'edition_number': request.form["edition_number"], 'isbn': request.form["isbn"], 'publisher': request.form["publisher"], 'publish_year': request.form["publish_year"], 'number_of_pages': request.form["number_of_pages"], 'language': request.form["language"]}

        err_message = Control().Input().book_edition(values, edition_number=edition_number, book_id=book_id)
        if err_message:
            return render_template("forms/book_edition_edit.html", values=values, title="Book Edition Adding", books=books, err_message=err_message)

        book_edition = BookEditionObj(values["book_id"], values["edition_number"], values["isbn"], values["publisher"], values["publish_year"], values["number_of_pages"], values["language"])
        book_id, edition_number = db.book_edition.update(book_id, edition_number, book_edition)
        return redirect(url_for("book_edition_page", book_id=book_id, edition_number=edition_number))


def book_edition_delete_page(book_id, edition_number):
    db = current_app.config["db"]
    db.book_edition.delete(book_id, edition_number)
    return redirect(url_for("book_page", book_key=book_id))


def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        db = current_app.config["db"]
        user = db.customer.get_row("USERNAME", username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password_hash):
                login_user(user)
                flash("You have logged in successfully")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)

        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))


def signup_page():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        user_username = request.form["inputUsername"]
        user_password = request.form["inputPassword"]
        user_email = request.form["inputEmail"]
        user_name = request.form["inputName"]
        user_surname = request.form["inputSurname"]
        user_phone = request.form["inputPhone"]
        user_DOB = request.form["inputDOB"]
        user_gender = request.form["inputGender"]

        sign_up(user_username, user_password, user_email, user_name, user_surname, user_phone, user_DOB, user_gender)
        return redirect(url_for("home_page"))
