from flask import current_app, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from passlib.hash import pbkdf2_sha256 as hasher
from forms import LoginForm, SignUpForm
from views.customer_view import customer_take_info_from_form


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

        db = current_app.config["db"]
        values = customer_take_info_from_form(form)
        check_dict = {'USERNAME': 0, 'EMAIL': 1, 'PHONE': 3}
        for attr, val in check_dict.items():
            if db.customer.get_row("*", attr, values[1][val]) is not None:
                flash("This {} is already in use".format(attr.lower()), 'danger')
                return render_template("customer/signup.html", form=form)

        person_id = db.person.add(*values[0])
        customer_id = db.customer.add(person_id, *values[1], True)
        db.transaction.add_empty(customer_id)

        flash("You have registered successfully", "success")
        return redirect(url_for("home_page"))

    return render_template("customer/signup.html", form=form)
