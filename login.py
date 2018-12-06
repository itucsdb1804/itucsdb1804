from passlib.hash import pbkdf2_sha256 as hasher
import psycopg2 as dbapi2
import os
import sys
from flask import flash, current_app


def check_password(username, pass_input):
    
    db = current_app.config["db"]
    pass_hash = db.customer.get_row("USERNAME", username, "PASS_HASH")
    if pass_hash != None:
        print(pass_hash)
        return hasher.verify(pass_input, pass_hash)
    else:
        print("Hatali Parola")
        return False


def set_password(username, password):
    pass_hash = hasher.hash(password)
    db = current_app.config["db"]
    db.customer.update([pass_hash, username], "USERNAME", 1, "PASS_HASH")


def sign_up(username, password, email, name, surname, phone, dob, gender, nationality="EMPTY"):
    pass_hash = hasher.hash(password)
    print(pass_hash)
    print(len(pass_hash))

    db = current_app.config["db"]

    person_id = db.person.add(name, surname, gender, dob, nationality)
    db.customer.add(person_id, username, email, pass_hash, phone, True)


def login(username, password):
    if check_password(username, password):
        flash("You have successfully logged in.")
        return True
    else:
        flash("You have entered a wrong password or username.")
        return False


def change_password(username, pass_old, pass_new):
    if check_password(username, pass_old) != True:
        print("You have entered a wrong password.")
    else:
        set_password(username, pass_new)
        print("Password has successfully changed.")
