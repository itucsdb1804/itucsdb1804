from flask import current_app, render_template, request, redirect, url_for, session, flash
from forms import LoginForm
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import login_user, logout_user, login_required, current_user
from login import check_password, sign_up

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        db = current_app.config["db"]
        user = db.customer.get_row("*", "USERNAME", username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password_hash):
                login_user(user)
                flash("You have logged in successfully")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)

        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))


def signup_page():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        user_username = request.form["inputUsername"]
        user_password = request.form["inputPassword"]
        user_email = request.form["inputEmail"]
        user_name = request.form["inputName"]
        user_surname = request.form["inputSurname"]
        user_phone = request.form["inputPhone"]
        user_DOB = request.form["inputDOB"]
        user_gender = request.form["inputGender"]

        sign_up(user_username, user_password, user_email, user_name, user_surname, user_phone, user_DOB, user_gender)
        return redirect(url_for("home_page"))