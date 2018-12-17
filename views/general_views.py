from flask import current_app, render_template


def home_page():
    return render_template("home.html")


def persons_page():
    db = current_app.config["db"]
    persons = db.person.get_table()
    return render_template("persons.html", persons=persons)


