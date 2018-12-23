from flask import current_app, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from passlib.hash import pbkdf2_sha256 as hasher
from forms import SignUpForm

@login_required
def customers_page():
    if not current_user.is_admin:
        return abort(401)
    db = current_app.config["db"]
    customers = db.customer.get_table("*", "IS_ACTIVE", [True])
    return render_template("customer/customers.html", customers=customers)


def customer_take_info_from_form(form):
    return ([form.data["p_name"], form.data["p_surname"], form.data["p_gender"], form.data["p_dob"], form.data["p_nationality"]], [form.data["c_username"], form.data["c_email"], hasher.hash(form.data["c_password"]), form.data["c_phone"]])


@login_required
def edit_customer_page(customer_id):

    if customer_id != current_user.id and not current_user.is_admin:
        return abort(401)

    db = current_app.config["db"]
    customer_obj = db.customer.get_row("*", "CUSTOMER_ID", customer_id)
    person_obj = db.person.get_row("*", "PERSON_ID", customer_obj.person_id)

    form = SignUpForm()
    if form.validate_on_submit():
        values = customer_take_info_from_form(form)
        db.person.update(["PERSON_NAME", "SURNAME", "GENDER", "DATE_OF_BIRTH", "NATIONALITY"], values[0], "PERSON_ID", person_obj.person_id)
        db.customer.update(["USERNAME", "EMAIL", "PASS_HASH", "PHONE"], values[1], "CUSTOMER_ID", customer_id)

        flash("Informations are updated successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    return render_template("customer/customer_edit_form.html", form=form, person=person_obj, customer=customer_obj)


@login_required
def delete_customer_page(customer_id):
    if not current_user.is_admin:
        return abort(401)
    db = current_app.config["db"]
    db.customer.update("IS_ACTIVE", False, "CUSTOMER_ID", customer_id)
    return redirect(url_for("customers_page"))
