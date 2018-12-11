from passlib.hash import pbkdf2_sha256 as hasher
import psycopg2 as dbapi2
import os
import sys
from flask import flash, current_app


def sign_up(username, password, email, name, surname, phone, dob, gender, nationality=""):
    db = current_app.config["db"]
    pass_hash = hasher.hash(password)
    print(pass_hash)
    print(len(pass_hash))

    person_id = db.person.add(name, surname, gender, dob, nationality)
    db.customer.add(person_id, username, email, pass_hash, phone, True)



def login(username, password):
    if check_password(username, password):
        flash("You have successfully logged in.", 'success')
        return True
    else:
        flash("You have entered a wrong password or username.", 'danger')
        return False


def change_password(username, pass_old, pass_new):
    if check_password(username, pass_old) != True:
        flash("You have entered a wrong password.", 'danger')
    else:
        set_password(username, pass_new)
        flash("Password has successfully changed.", 'success')


def check_password(username, pass_input):
    db = current_app.config["db"]
    pass_hash = db.customer.get_row("USERNAME", username, "PASS_HASH")
    if pass_hash != None:
        return hasher.verify(pass_input, pass_hash)
    else:
        return False


def set_password(username, password):
    db = current_app.config["db"]
    pass_hash = hasher.hash(password)
    db.customer.update([pass_hash, username], "USERNAME", 1, "PASS_HASH")
