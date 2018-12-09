from flask import current_app, render_template, abort, request, redirect, url_for
import datetime
from table_operations.control import Control
from tables import BookObj, CommentObj

def books_page():
    db = current_app.config["db"]
    if request.method == "GET":
        books = db.book.get_table(with_author=True)
        return render_template("book/books.html", books=books)
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
        return render_template("book/book.html", book=book, authors=author_names, editions=editions, comments=comments, new_comment_values=new_comment_values)
    # If the new comment is added
    else:
        # Take values from add_comment form
        # TODO take customer_id from login system
        new_comment_values = {"customer_id": 1, "book_id": book_key, "comment_title": request.form["comment_title"], "comment_statement": request.form["comment_statement"], "rating": request.form["rating"]}

        comment_err_message = Control().Input().comment(new_comment_values)
        if comment_err_message:
            return render_template("book/book.html", book=book, authors=author_names, editions=editions, comments=comments, comment_err_message=comment_err_message, new_comment_values=new_comment_values)

        # Add comment to database
        comment = CommentObj(new_comment_values["customer_id"], new_comment_values["book_id"], new_comment_values["comment_title"], new_comment_values["comment_statement"], new_comment_values["rating"])
        db.comment.add(comment)

        return redirect(url_for("book_page", book_key=book_key))


def book_add_page():
    db = current_app.config["db"]
    err_message = None
    # Get authors because of selecting book's authors
    authors = []
    for author in db.author.get_table():
        authors.append((author, db.person.get_row(where_columns="PERSON_ID", where_values=author.person_id)))

    if request.method == "GET":
        values = {"book_name": "", "released_year": "", "explanation": "", "selected_author_ids": []}
        return render_template("book/book_form.html", min_year=1887, max_year=datetime.datetime.now().year, values=values, title="Book adding", err_message=err_message, authors=authors)
    else:
        values = {"book_name": request.form["book_name"], "released_year": request.form["released_year"], "explanation": request.form["explanation"], "selected_author_ids": request.form.getlist("selected_author_ids")}

        # Invalid input control
        err_message = Control().Input().book(values)
        if err_message:
            return render_template("book/book_form.html", min_year=1887, max_year=datetime.datetime.now().year, values=values, title="Book adding", err_message=err_message, authors=authors)

        book = BookObj(values["book_name"], values["released_year"], values["explanation"])

        book_id = db.book.add_book(book)
        for author_id in values["selected_author_ids"]:
            db.book_author.add(book_id, author_id)
        return redirect(url_for("books_page"))


def book_edit_page(book_key):
    db = current_app.config["db"]
    err_message = None
    # Get authors because of selecting book's authors
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
        return render_template("book/book_form.html", min_year=1887, max_year=datetime.datetime.now().year, values=values, title="Book editing", err_message=err_message, authors=authors)
    else:
        values = {"book_name": request.form["book_name"], "released_year": request.form["released_year"], "explanation": request.form["explanation"]}

        # Invalid input control
        err_message = Control().Input().book(values)
        if err_message:
            return render_template("book/book_form.html", min_year=1887, max_year=datetime.datetime.now().year, values=values, title="Book adding", err_message=err_message, authors=authors)

        book = BookObj(values["book_name"], values["released_year"], values["explanation"])
        book_id = db.book.update(book_key, book)
        db.book_author.delete(where_columns="BOOK_ID", where_values=book_id)
        for author_id in values["selected_author_ids"]:
            db.book_author.add(book_id, author_id)
        return redirect(url_for("book_page", book_key=book_key))


def book_delete_page(book_key):
    db = current_app.config["db"]
    db.book.delete(book_key)
    return redirect(url_for("books_page"))
