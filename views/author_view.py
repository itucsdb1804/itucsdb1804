from flask import current_app, render_template, abort, request, redirect, url_for, flash
from flask_login import current_user, login_required
from tables import AuthorObj, PersonObj
from forms import AuthorForm
from views.book_view import take_author_ids_and_names_by_book, take_categories_by_book


def authors_page():
    db = current_app.config["db"]

    author_list = []

    authors = db.author.get_table()
    for author in authors:
        person = db.person.get_row("*", ["PERSON_ID"], [author.person_id])
        author_list.append((author, person), )
    return render_template("author/authors.html", authors=author_list)


def author_take_info_from_form(form):
    '''
    p_name = form.data["p_name"]
    p_surname = form.data["p_surname"]
    p_gender = form.data["p_gender"]
    p_dob = form.data["p_dob"]
    p_nationality = form.data["p_nationality"]
    a_biography = form.data["author_biography"]
    '''
    return ([form.data["p_name"], form.data["p_surname"], form.data["p_gender"], form.data["p_dob"], form.data["p_nationality"]], form.data["a_biography"])


@login_required
def add_author():
    if not current_user.is_admin:
        return abort(401)
    db = current_app.config["db"]
    form = AuthorForm()
    if form.validate_on_submit():
        values = author_take_info_from_form(form)

        person_id = db.person.add(*values[0])
        db.author.add(person_id, values[1])

        flash("Author is added successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    empty_person = PersonObj()
    empty_author = AuthorObj("", "", "")
    return render_template("author/author_form.html", form=form, person=empty_person, author=empty_author)


@login_required
def author_edit_page(author_id):
    if not current_user.is_admin:
        return abort(401)
    db = current_app.config["db"]
    form = AuthorForm()
    author_obj = db.author.get_row("*", "AUTHOR_ID", author_id)
    person_obj = db.person.get_row("*", "PERSON_ID", author_obj.person_id)
    if form.validate_on_submit():
        values = author_take_info_from_form(form)
        db.person.update(["PERSON_NAME", "SURNAME", "GENDER", "DATE_OF_BIRTH", "NATIONALITY"], values[0], "PERSON_ID", author_obj.person_id)
        db.author.update("BIOGRAPHY", values[1], "AUTHOR_ID", author_id)

        flash("Author is updated successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    return render_template("author/author_form.html", form=form, person=person_obj, author=author_obj)


@login_required
def author_delete_page(author_id):
    if not current_user.is_admin:
        abort(401)
    db = current_app.config["db"]
    db.author.delete(author_id)
    return redirect(url_for("authors_page"))


def books_by_author_page(author_id):
    db = current_app.config["db"]
    author = db.author.get_row(where_columns="AUTHOR_ID", where_values=author_id)
    person = db.person.get_row(where_columns="PERSON_ID", where_values=author.person_id)
    if request.method == "GET":
        book_author_list = db.book_author.get_table(where_columns="AUTHOR_ID", where_values=author_id)
        books = []
        for book_author in book_author_list:
            books.append((db.book.get_row(book_author.book_id), take_author_ids_and_names_by_book(book_author.book_id), take_categories_by_book(book_author.book_id)))
        return render_template("book/books.html", books=books, title=person.person_name + " " + person.person_surname + "'s Books")
    else:
        form_book_keys = request.form.getlist("book_keys")
        for form_book_key in form_book_keys:
            db.book.delete(form_book_key)
        return redirect(url_for("books_page"))
