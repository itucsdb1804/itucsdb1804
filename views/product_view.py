from flask import current_app, render_template, abort, request, redirect, url_for
from table_operations.control import Control
from tables import ProductObj


def product_page(book_id, edition_number):
    db = current_app.config["db"]

    # Take product information
    product = db.product.get_row(book_id, edition_number)
    # If there is no product with this book_key, abort 404 page
    if product is None:
        abort(404)

    # Take necessary information
    pass

    # If the product page is displayed
    if request.method == "GET":
        # Blank buying form
        buying_values = {}
        return render_template("product/product.html", product=product, buying_values=buying_values)
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

    book_editions = db.book_edition.get_table()

    # If the product add page is displayed
    if request.method == "GET":
        values = {"book_id": "", "edition_number": "", "remaining": "", "actual_price": "", "number_of_sells": "", "product_explanation": "", "is_active": ""}
        return render_template("product/product_form.html", title="Product Adding", values=values, book_editions=book_editions)
    # If product is added
    else:
        # Take values from buying form
        values = {"book_id": request.form["book_id"], "edition_number": request.form["edition_number"], "remaining": request.form["remaining"], "actual_price": request.form["actual_price"], "number_of_sells": request.form["number_of_sells"], "product_explanation": request.form["product_explanation"], "is_active": request.form["is_active"]}

        # Invalid input control
        err_message = Control().Input().product(values)
        if err_message:
            return render_template("product/product_form.html", title="Product Adding", values=values, book_editions=book_editions, err_message=err_message)

        product = ProductObj(values["book_id"], values["edition_number"], values["remaining"], values["actual_price"], values["number_of_sells"], values["product_explanation"], values["is_active"])
        book_id, edition_number = db.product.add(product)
        return redirect(url_for("product_page", book_id=book_id, edition_number=edition_number))


def product_edit_page(book_id, edition_number):
    db = current_app.config["db"]

    book_editions = db.book_edition.get_table()

    # If the product add page is displayed
    if request.method == "GET":
        # Take product information
        product = db.product.get_row(book_id, edition_number)
        # If there is no product with this book_key, abort 404 page
        if product is None:
            abort(404)

        values = {"book_id": product.book_id, "edition_number": product.edition_number, "remaining": product.remaining, "actual_price": product.actual_price, "number_of_sells": product.number_of_sells, "product_explanation": product.product_explanation, "is_active": product.is_active}
        return render_template("product/product_form.html", title="Product Adding", values=values, book_editions=book_editions)
    # If product is added
    else:
        # Take values from buying form
        values = {"book_id": request.form["book_id"], "edition_number": request.form["edition_number"], "remaining": request.form["remaining"], "actual_price": request.form["actual_price"], "number_of_sells": request.form["number_of_sells"], "product_explanation": request.form["product_explanation"], "is_active": request.form["is_active"]}

        # Invalid input control
        err_message = Control().Input().product(values)
        if err_message:
            return render_template("product/product_form.html", title="Product Adding", values=values, book_editions=book_editions, err_message=err_message)

        product = ProductObj(values["book_id"], values["edition_number"], values["remaining"], values["actual_price"], values["number_of_sells"], values["product_explanation"], values["is_active"])
        book_id, edition_number = db.product.add(product)
        return redirect(url_for("product_page", book_id=book_id, edition_number=edition_number))


def product_delete_page(book_id, edition_number):
    db = current_app.config["db"]
    db.product.delete(book_id, edition_number)
    return redirect(url_for("book_page", book_key=book_id))
