from flask import current_app, render_template, abort, request, redirect, url_for
from table_operations.control import Control
from tables import ProductObj


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
    product = db.product.get_row(book_id, edition_number)
    edition = db.book_edition.get_row(book_id, edition_number)
    book = db.book.get_row(book_id)
    author_names = []  # TODO Kitabın bütün yazarlarını alma fonksiyonu
    for book_author in db.book_author.get_table(where_columns="BOOK_ID", where_values=book_id):
        for author in db.author.get_table(where_columns="AUTHOR_ID", where_values=book_author.author_id):
            for person in db.person.get_table(where_columns="PERSON_ID", where_values=author.person_id):
                author_names.append(person.person_name + " " + person.person_surname)
    # If there is not product, edition, or book with this book_key and edition_number, abort 404 page
    if product is None or edition is None or book is None:
        abort(404)

    # Take necessary information
    pass

    # If the product page is displayed
    if request.method == "GET":
        # Blank buying form
        buying_values = {}
        return render_template("product/product.html", product=product, book=book, edition=edition, authors=author_names, buying_values=buying_values)
    # If it is added to shopping cart
    else:
        # Take values from buying form
        buying_values = {}

        # Invalid input control
        err_message = Control().Input().buying(buying_values)
        if err_message:
            return render_template("product/product.html", product=product, buying_values=buying_values, err_message=err_message)

        # Add product to shopping cart
        pass

        return redirect(url_for("product_page", book_id=book_id, edition_number=edition_number))


def product_add_page():
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


def product_edit_page(book_id, edition_number):
    db = current_app.config["db"]

    # Take product information
    product = db.product.get_row(book_id, edition_number)
    # If there is no product with this book_key, abort 404 page
    if product is None:
        abort(404)

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


def product_delete_page(book_id, edition_number):
    db = current_app.config["db"]
    db.product.delete(book_id, edition_number)
    return redirect(url_for("book_page", book_key=book_id))
