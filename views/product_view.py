from flask import current_app, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control
from tables import ProductObj, TransactionProductObj
from views.book_view import take_categories_by_book, take_author_ids_and_names_by_book


def products_page():
    db = current_app.config["db"]
    if request.method == "GET":
        tables = db.product.get_products_all_info()
        return render_template("product/products.html", tables=tables)
    else:
        return redirect(url_for("products_page"))


def product_page(book_id, edition_number):
    db = current_app.config["db"]

    # Take product information
    book = db.book.get_row(book_id)
    edition = db.book_edition.get_row(book_id, edition_number)
    product = db.product.get_row(book_id, edition_number)
    author_names = take_author_ids_and_names_by_book(book_id)
    categories = take_categories_by_book(book_id)

    # If there is not product, edition, or book with this book_key and edition_number, abort 404 page
    if product is None or edition is None or book is None:
        return abort(404)

    # If the product page is displayed
    if request.method == "GET":
        # Blank buying form
        buying_values = {}
        return render_template("product/product.html", title=(book.book_name+" Product Page"), product=product, book=book, edition=edition, authors=author_names, categories=categories, buying_values=buying_values)
    # If it is added to shopping cart
    else:
        if not current_user.is_authenticated or not product.is_active:
            return abort(401)
        transaction = db.transaction.get_row(where_columns=["CUSTOMER_ID", "IS_COMPLETED"], where_values=[current_user.id, False])
        # Take values from buying form
        buying_values = {"piece": request.form["piece"]}

        transaction_product = TransactionProductObj(transaction.transaction_id, product.book_id, product.edition_number, buying_values["piece"], product.actual_price)

        # Invalid input control
        err_message = Control().Input().buying(buying_values, transaction_product=transaction_product, product=product)
        if err_message:
            return render_template("product/product.html", title=(book.book_name+" Product Page"), product=product, book=book, edition=edition, authors=author_names, categories=categories, buying_values=buying_values, err_message=err_message)

        # Add product to shopping cart
        if db.transaction_product.get_row(where_columns=["TRANSACTION_ID", "BOOK_ID", "EDITION_NUMBER"], where_values=[transaction_product.transaction_id, transaction_product.book_id, transaction_product.edition_number]):
            db.transaction_product.update(update_columns=["PIECE"], new_values=[transaction_product.piece], where_columns=["TRANSACTION_ID", "BOOK_ID", "EDITION_NUMBER"], where_values=[transaction_product.transaction_id, transaction_product.book_id, transaction_product.edition_number])
        else:
            db.transaction_product.add(transaction_product)

        return redirect(url_for("product_page", book_id=book_id, edition_number=edition_number))


@login_required
def product_add_page():
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]

    books_and_editions = []
    for book in db.book.get_table():
        books_and_editions.append({'book': book, 'editions': db.book_edition.get_table(where_columns=db.book_edition.columns["book_id"], where_values=book.book_id)})

    # If the product add page is displayed
    if request.method == "GET":
        values = {"book_and_edition": "", "remaining": "", "actual_price": "", "product_explanation": "", "is_active": ""}
        return render_template("product/product_form.html", title="Product Adding", values=values, books_and_editions=books_and_editions)
    # If product is added
    else:
        # Take values from buying form
        values = {"book_and_edition": request.form["book_and_edition"], "remaining": request.form["remaining"], "actual_price": request.form["actual_price"], "product_explanation": request.form["product_explanation"], "is_active": request.form.getlist("is_active") == ['active']}

        # Invalid input control
        err_message = Control().Input().product(values)
        if err_message:
            return render_template("product/product_form.html", title="Product Adding", values=values, books_and_editions=books_and_editions, err_message=err_message)

        product = ProductObj(values["book_and_edition"].split()[0], values["book_and_edition"].split()[1], values["remaining"], values["actual_price"], 0, values["product_explanation"], values["is_active"])
        book_id, edition_number = db.product.add(product)
        return redirect(url_for("product_page", book_id=book_id, edition_number=edition_number))


@login_required
def product_edit_page(book_id, edition_number):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]

    # Take product information
    product = db.product.get_row(book_id, edition_number)
    # If there is no product with this book_key, abort 404 page
    if product is None:
        return abort(404)

    books_and_editions = []
    for book in db.book.get_table():
        books_and_editions.append({'book': book, 'editions': db.book_edition.get_table(where_columns=db.book_edition.columns["book_id"], where_values=book.book_id)})

    # If the product add page is displayed
    if request.method == "GET":
        values = {"book_and_edition": str(product.book_id) + " " + str(product.edition_number), "remaining": product.remaining, "actual_price": product.actual_price, "product_explanation": product.product_explanation, "is_active": product.is_active}
        return render_template("product/product_form.html", title="Product Editing", values=values, books_and_editions=books_and_editions)
    # If product is added
    else:
        # Take values from buying form
        values = {"book_and_edition": request.form["book_and_edition"], "remaining": request.form["remaining"], "actual_price": request.form["actual_price"], "product_explanation": request.form["product_explanation"], "is_active": request.form.getlist("is_active") == ['active']}

        # Invalid input control
        err_message = Control().Input().product(values, is_new=False, book_and_edition=str(product.book_id) + " " + str(product.edition_number))
        if err_message:
            return render_template("product/product_form.html", title="Product Editing", values=values, books_and_editions=books_and_editions, err_message=err_message)

        product = ProductObj(product.book_id, product.edition_number, values["remaining"], values["actual_price"], product.number_of_sells, values["product_explanation"], values["is_active"])
        book_id, edition_number = db.product.update(product.book_id, product.edition_number, product)
        return redirect(url_for("product_page", book_id=book_id, edition_number=edition_number))


@login_required
def product_delete_page(book_id, edition_number):
    if not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    product = db.product.get_row(book_id, edition_number)
    product.is_active = False
    db.product.update(book_id, edition_number, product)
    return redirect(url_for("book_page", book_key=book_id))
