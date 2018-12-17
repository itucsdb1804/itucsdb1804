from flask import current_app, render_template, abort, request, redirect, url_for, flash
from tables import CustomerObj, PersonObj
from forms import SignUpForm


def customers_page():
    db = current_app.config["db"]
    customers = db.customer.get_table()
    return render_template("customer/customers.html", customers=customers)


def customer_take_info_from_form(form):
    '''
    p_name = form.data["p_name"]
    p_surname = form.data["p_surname"]
    p_gender = form.data["p_gender"]
    p_dob = form.data["p_dob"]
    p_nationality = form.data["p_nationality"]
    c_username = form.data["c_username"]
    c_email = form.data["c_email"]
    c_password = form.data["c_password"]
    c_phone = form.data["c_phone"]
    '''
    return ([form.data["p_name"], form.data["p_surname"], form.data["p_gender"], form.data["p_dob"], form.data["p_nationality"]], [form.data["c_username"], form.data["c_email"], form.data["c_password"], form.data["c_phone"]])



def edit_customer_page(customer_id):
    db = current_app.config["db"]
    form = SignUpForm()
    customer_obj = db.customer.get_row("*", "CUSTOMER_ID", customer_id)
    person_obj = db.person.get_row("*", "PERSON_ID", customer_obj.person_id)
    if form.validate_on_submit():
        values = customer_take_info_from_form(form)
        db.person.update(["PERSON_NAME", "SURNAME", "GENDER", "DATE_OF_BIRTH", "NATIONALITY"], values[0], "PERSON_ID", person_obj.person_id)
        db.customer.update(["USERNAME", "EMAIL", "PASS_HASH", "PHONE"], values[1], "CUSTOMER_ID", customer_id)

        flash("Informations are updated successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    return render_template("customer/customer_edit_form.html", form=form, person=person_obj, customer=customer_obj)
        


def delete_customer_page(customer_id):
    db = current_app.config["db"]
    db.customer.delete(customer_id)
    return redirect(url_for("customers_page"))