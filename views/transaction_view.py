from flask import current_app, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from table_operations.control import Control


@login_required
def transaction_page():
    db = current_app.config["db"]

    transaction = db.transaction.get_row(where_columns=["CUSTOMER_ID", "IS_COMPLETED"], where_values=[current_user.id, False])
    update_price_by_transaction(transaction.transaction_id)
    transaction_products_with, total_price = get_tproducts_with_book_and_edition_by_transaction(transaction.transaction_id)

    control_err_message = control_piece_of_product_in_transaction(transaction.transaction_id)
    if control_err_message is not None:
        print("my output", control_err_message)
        return render_template("transaction/transaction.html", transaction_products_with=transaction_products_with, total_price=total_price, err_message=control_err_message)

    return render_template("transaction/transaction.html", transaction_products_with=transaction_products_with, total_price=total_price)


@login_required
def transaction_next_page():
    db = current_app.config["db"]

    transaction = db.transaction.get_row(where_columns=["CUSTOMER_ID", "IS_COMPLETED"], where_values=[current_user.id, False])
    update_price_by_transaction(transaction.transaction_id)
    addresses = get_addresses_by_customer(current_user.id)
    print(addresses)
    control_err_message = control_piece_of_product_in_transaction(transaction.transaction_id)
    if control_err_message is not None:
        return redirect(url_for("transaction_page"))

    if request.method == "GET":
        return render_template("transaction/transaction_form.html", addresses=addresses, values={'transaction_explanation': ""})
    else:
        values = {'address_id': request.form['address_id'], 'payment_type': request.form['payment_type'], 'transaction_explanation': request.form['transaction_explanation']}
        err_message = Control().Input().transaction(values, transaction=transaction)
        if err_message:
            return render_template("transaction/transaction_form.html", addresses=addresses, err_message=err_message, values=values)

        # Decrease the order number of products
        for tp in db.transaction_product.get_table(where_columns=["TRANSACTION_ID"], where_values=[transaction.transaction_id]):
            product = db.product.get_row(tp.book_id, tp.edition_number)
            db.product.update_piece_and_remainig(book_id=tp.book_id, edition_number=tp.edition_number, new_remaining=product.remaining - tp.piece, new_sold=product.number_of_sells + tp.piece)

        db.transaction.update(update_columns=["ADDRESS_ID", "TRANSACTION_TIME", "PAYMENT_TYPE", "TRANSACTION_EXPLANATION", "IS_COMPLETED"], new_values=[values['address_id'], 'CURRENT_TIMESTAMP', values['payment_type'], values['transaction_explanation'], True], where_columns=["TRANSACTION_ID"], where_values=[transaction.transaction_id])
        db.transaction.add_empty(current_user.id)
        return render_template("transaction/transaction.html", message="Shopping completed")


def get_tproducts_with_book_and_edition_by_transaction(t_id):
    db = current_app.config["db"]
    transaction_products = []
    total_price = 0
    for tproduct in db.transaction_product.get_table(where_columns=["TRANSACTION_ID"], where_values=[t_id]):
        transaction_products.append({'transaction_product': tproduct, 'book': db.book.get_row(tproduct.book_id), 'book_edition': db.book_edition.get_row(tproduct.book_id, tproduct.edition_number)})
        total_price += tproduct.piece*tproduct.unit_price
    return transaction_products, total_price


def tp_delete_page(transaction_id, book_id, edition_number):
    db = current_app.config["db"]
    db.transaction_product.delete(transaction_id, book_id, edition_number)
    return redirect(url_for("transaction_page"))


def update_price_by_transaction(t_id):
    db = current_app.config["db"]
    tps = db.transaction_product.get_table(where_columns=["TRANSACTION_ID"], where_values=[t_id])
    for tp in tps:
        db.transaction_product.update(update_columns=["UNIT_PRICE"], new_values=[db.product.get_row(tp.book_id, tp.edition_number).actual_price], where_columns=["TRANSACTION_ID", "BOOK_ID", "EDITION_NUMBER"], where_values=[tp.transaction_id, tp.book_id, tp.edition_number])


def get_addresses_by_customer(customer_id):
    db = current_app.config["db"]
    addresses = []
    for address in db.customer_address.get_table(where_columns=["CUSTOMER_ID"], where_values=[customer_id]):
        addresses.append(db.address.get_row(where_columns=["ADDRESS_ID"], where_values=[address.address_id]))
    return addresses


def control_piece_of_product_in_transaction(transaction_id):
    db = current_app.config["db"]
    tps = db.transaction_product.get_table(where_columns=["TRANSACTION_ID"], where_values=[transaction_id])
    for tp in tps:
        if tp.piece > db.product.get_row(tp.book_id, tp.edition_number).remaining:
            print(tp.piece, db.product.get_row(tp.book_id, tp.edition_number).remaining)
            return "There is not enough from \"%s's %s. edition\"" %(db.book.get_row(tp.book_id).book_name, tp.edition_number)
    return None
