from flask import current_app, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from passlib.hash import pbkdf2_sha256 as hasher
from forms import LoginForm, SignUpForm
from login import sign_up


def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        db = current_app.config["db"]
        user = db.customer.get_row("*", "USERNAME", username)
        if user is not None and user.is_active:
            password = form.data["password"]
            remember = form.data["remember_me"]
            if hasher.verify(password, user.password_hash):
                login_user(user, remember)
                flash("You have logged in successfully", "success")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)

            flash("You have entered a wrong username or password.", 'danger')
            return redirect(url_for("login_page"))

        flash("Invalid credentials.", "danger")
    return render_template("customer/login.html", form=form)


@login_required
def logout_page():
    logout_user()
    flash("You have logged out.", "info")
    return redirect(url_for("home_page"))


def signup_page():
    form = SignUpForm()

    if form.validate_on_submit():
        u_username = form.data["c_username"]
        u_password = form.data["c_password"]
        u_email = form.data["c_email"]
        u_phone = form.data["c_phone"]
        u_name = form.data["p_name"]
        u_surname = form.data["p_surname"]
        u_dob = form.data["p_dob"]
        u_gender = form.data["p_gender"]
        u_nationality = form.data["p_nationality"]

        db = current_app.config["db"]
        if db.customer.get_row("*", "USERNAME", u_username) is not None:
            flash("This username is already taken", 'danger')
            return render_template("customer/signup.html", form=form)
        if db.customer.get_row("*", "EMAIL", u_email) is not None:
            flash("This e-mail address is already using by another user", 'danger')
            return render_template("customer/signup.html", form=form)
        if db.customer.get_row("*", "PHONE", u_phone) is not None:
            flash("This phone number is already using by another user", 'danger')
            return render_template("customer/signup.html", form=form)

        sign_up(u_username, u_password, u_email, u_name, u_surname, u_phone, u_dob, u_gender, u_nationality)
        flash("You have registered successfully", "success")
        return redirect(url_for("home_page"))

    return render_template("customer/signup.html", form=form)
