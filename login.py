from flask import current_app, flash
from passlib.hash import pbkdf2_sha256 as hasher


def sign_up(username, password, email, name, surname, phone, dob, gender, nationality):
    db = current_app.config["db"]
    pass_hash = hasher.hash(password)

    person_id = db.person.add(name, surname, gender, dob, nationality)
    customer_id = db.customer.add(person_id, username, email, pass_hash, phone, True)
    db.transaction.add_empty(customer_id)


def change_password(username, pass_old, pass_new):
    if not check_password(username, pass_old):
        return flash("You have entered a wrong password.", 'danger')

    set_password(username, pass_new)
    return flash("Password has successfully changed.", 'success')


def check_password(username, pass_input):
    db = current_app.config["db"]
    pass_hash = db.customer.get_row("USERNAME", username, "PASS_HASH")
    if pass_hash is not None:
        return hasher.verify(pass_input, pass_hash)
    return False


def set_password(username, password):
    db = current_app.config["db"]
    pass_hash = hasher.hash(password)
    db.customer.update([pass_hash, username], "USERNAME", 1, "PASS_HASH")
