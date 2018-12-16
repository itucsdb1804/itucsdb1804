from flask import current_app, render_template, abort, request, redirect, url_for
from table_operations.control import Control
from tables import BookEditionObj
from flask_login import current_user, login_required


def book_edition_page(book_id, edition_number):
    return redirect(url_for('product_page', book_id=book_id, edition_number=edition_number))


def book_edition_add_page():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(401)

    db = current_app.config["db"]
    err_message = None
    books = db.book.get_table()
    if request.method == "GET":
        values = {"book_id": "", "edition_number": "", "isbn": "", "publisher": "", "publish_year": "", "number_of_pages": "", "language": ""}
        return render_template("book_edition/book_edition_form.html", values=values, title="Book Edition Adding", books=books, err_message=err_message)
    else:
        values = {'book_id': int(request.form["book_id"]), 'edition_number': request.form["edition_number"], 'isbn': request.form["isbn"], 'publisher': request.form["publisher"], 'publish_year': request.form["publish_year"], 'number_of_pages': request.form["number_of_pages"], 'language': request.form["language"]}
        err_message = Control().Input().book_edition(values)
        if err_message:
            return render_template("book_edition/book_edition_form.html", values=values, title="Book Edition Adding", books=books, err_message=err_message)

        book_edition = BookEditionObj(values["book_id"], values["edition_number"], values["isbn"], values["publisher"], values["publish_year"], values["number_of_pages"], values["language"])
        book_id, edition_number = db.book_edition.add(book_edition)
        return redirect(url_for("book_edition_page", book_id=book_id, edition_number=edition_number))


def book_edition_edit_page(book_id, edition_number):
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(401)

    db = current_app.config["db"]
    err_message = None
    books = db.book.get_table()
    if request.method == "GET":
        book_edition = db.book_edition.get_row(book_id, edition_number)
        if book_edition is None:
            abort(404)
        values = {"book_id": book_edition.book_id, "edition_number": book_edition.edition_number, "isbn": book_edition.isbn, "publisher": book_edition.publisher, "publish_year": book_edition.publish_year, "number_of_pages": book_edition.number_of_pages, "language": book_edition.language}
        return render_template("book_edition/book_edition_form.html", values=values, title="Book Edition Adding", books=books, err_message=err_message)
    else:
        values = {'book_id': request.form["book_id"], 'edition_number': request.form["edition_number"], 'isbn': request.form["isbn"], 'publisher': request.form["publisher"], 'publish_year': request.form["publish_year"], 'number_of_pages': request.form["number_of_pages"], 'language': request.form["language"]}

        err_message = Control().Input().book_edition(values, edition_number=edition_number, book_id=book_id)
        if err_message:
            return render_template("book_edition/book_edition_form.html", values=values, title="Book Edition Adding", books=books, err_message=err_message)

        book_edition = BookEditionObj(values["book_id"], values["edition_number"], values["isbn"], values["publisher"], values["publish_year"], values["number_of_pages"], values["language"])
        book_id, edition_number = db.book_edition.update(book_id, edition_number, book_edition)
        return redirect(url_for("book_edition_page", book_id=book_id, edition_number=edition_number))


def book_edition_delete_page(book_id, edition_number):
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(401)

    db = current_app.config["db"]
    db.book_edition.delete(book_id, edition_number)
    return redirect(url_for("book_page", book_key=book_id))