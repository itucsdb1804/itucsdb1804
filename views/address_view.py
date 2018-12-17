from flask import current_app, render_template, flash, request, url_for, redirect, abort
from flask_login import current_user, login_required
from forms import AddressForm
from tables import AddressObj

@login_required
def addresses_page():
    if not current_user.is_admin:
        return abort(401)
    db = current_app.config["db"]
    addresses = db.address.get_table()
    return render_template("address/addresses.html", addresses=addresses)



def address_take_info_from_form(form):
    return [form.data["address_name"], form.data["country"], form.data["city"], form.data["district"], form.data["neighborhood"], form.data["avenue"], form.data["street"], form.data["addr_num"], form.data["zipcode"], form.data["explanation"]]


@login_required
def add_address():
    db = current_app.config["db"]
    form = AddressForm()
    empty_address = AddressObj("", "", "", "", "", "", "", "", "", "", "")
    if form.validate_on_submit():
        values = address_take_info_from_form(form)

        address_id = db.address.add(*values)
        db.customer_address.add(current_user.id, address_id)

        flash("Address is added successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    return render_template("address/address_form.html", form=form, address=empty_address)


@login_required
def address_edit_page(address_id):
    db = current_app.config["db"]
    customer_id = db.customer_address.get_row("CUSTOMER_ID", "ADDRESS_ID", address_id)
    if current_user.id != customer_id and not current_user.is_admin:
        return abort(401)

    form = AddressForm()
    address_obj = db.address.get_row("*", "ADDRESS_ID", address_id)
    if form.validate_on_submit():
        values = address_take_info_from_form(form)
        db.address.update(["ADDRESS_NAME", "COUNTRY", "CITY", "DISTRICT", "NEIGHBORHOOD", "AVENUE", "STREET", "ADDR_NUMBER", "ZIPCODE", "EXPLANATION"], values, "ADDRESS_ID", address_obj.address_id)

        flash("Address is updated successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    return render_template("address/address_form.html", form=form, address=address_obj)



@login_required
def address_delete_page(address_id):
    db = current_app.config["db"]
    customer_id = db.customer_address.get_row("CUSTOMER_ID", "ADDRESS_ID", address_id)
    if current_user.id != customer_id and not current_user.is_admin:
        return abort(401)

    db.customer_address.delete(address_id)
    db.address.delete(address_id)
    return redirect(url_for("addresses_page"))
