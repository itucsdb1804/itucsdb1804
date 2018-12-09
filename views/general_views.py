from flask import current_app, render_template, abort, request, redirect, url_for, session, flash


def home_page():
    return render_template("home.html")


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


