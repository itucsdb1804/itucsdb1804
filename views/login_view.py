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
                flash("You have logged in successfully", "success")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)

        flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.", "info")
    return redirect(url_for("home_page"))


def signup_page():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        u_username = request.form["inputUsername"]
        u_password = request.form["inputPassword"]
        u_email = request.form["inputEmail"]
        u_name = request.form["inputName"]
        u_surname = request.form["inputSurname"]
        u_phone = request.form["inputPhone"]
        u_DOB = request.form["inputDOB"]
        u_gender = request.form["inputGender"]

        sign_up(u_username, u_password, u_email, u_name, u_surname, u_phone, u_DOB, u_gender)
        flash("You have registered successfully", "success")
        return redirect(url_for("home_page"))