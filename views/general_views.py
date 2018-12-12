from flask import current_app, render_template, abort, request, redirect, url_for, session, flash


def home_page():
    return render_template("home.html")


def addresses_page():
    db = current_app.config["db"]
    addresses = db.address.get_table()
    return render_template("addresses.html", addresses=addresses)


def persons_page():
    db = current_app.config["db"]
    persons = db.person.get_table()
    return render_template("persons.html", persons=persons)


