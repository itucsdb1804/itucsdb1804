from flask import current_app, render_template, request, redirect, url_for
from views.book_view import take_author_ids_and_names_by_book, take_categories_by_book


def books_by_category_page(category_id):
    db = current_app.config["db"]
    category = db.category.get_row(where_columns="CATEGORY_ID", where_values=category_id)
    if request.method == "GET":
        book_category_list = db.book_category.get_table(where_columns="CATEGORY_ID", where_values=category_id)
        books = []
        for book_category in book_category_list:
            books.append((db.book.get_row(book_category.book_id), take_author_ids_and_names_by_book(book_category.book_id), take_categories_by_book(book_category.book_id)))
        return render_template("book/books.html", books=books, title="Books in category of " + category.category_name)
    else:
        form_book_keys = request.form.getlist("book_keys")
        for form_book_key in form_book_keys:
            db.book.delete(form_book_key)
        return redirect(url_for("books_page"))


def categories_page():
    db = current_app.config["db"]
    categories = db.category.get_table()
    return render_template("category/categories.html", categories=categories)
