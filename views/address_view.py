from flask import current_app, render_template, flash, request, url_for, redirect, abort
from flask_login import current_user, login_required
from forms import AddressForm
from tables import AddressObj, CustomerAddressObj

@login_required
def addresses_page():
    db = current_app.config["db"]
    addresses = []
    if not current_user.is_admin:
        address_ids = db.customer_address.get_table("ADDRESS_ID", "CUSTOMER_ID", current_user.id)
        for addr_id in address_ids:
            addresses.append(db.address.get_row("*", "ADDRESS_ID", addr_id))
    else:
        addresses = db.address.get_table()
    return render_template("address/addresses.html", addresses=addresses)



def address_take_info_from_form(form, x):
    return [form.data["address_name"], form.data["country"], form.data["city"], form.data["district"], form.data["neighborhood"], form.data["avenue"], form.data["street"], form.data["addr_num"], form.data["zipcode"], x["explanation"]]


@login_required
def add_address():
    db = current_app.config["db"]
    form = AddressForm()
    empty_address = AddressObj("", "", "", "", "", "", "", "", "", "", "")
    if form.validate_on_submit():
        values = address_take_info_from_form(form, request.form)

        db.address.add(*values)
        address_id = db.address.get_table()[-1].address_id
        db.customer_address.add(CustomerAddressObj(current_user.id, address_id))

        flash("Address is added successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    return render_template("address/address_form.html", form=form, address=empty_address, head_title="Add new address")


@login_required
def address_edit_page(address_id):
    db = current_app.config["db"]
    customer_id = db.customer_address.get_row("CUSTOMER_ID", "ADDRESS_ID", address_id)
    if current_user.id != customer_id and not current_user.is_admin:
        return abort(401)

    form = AddressForm()
    address_obj = db.address.get_row("*", "ADDRESS_ID", address_id)
    if form.validate_on_submit():
        values = address_take_info_from_form(form, request.form)
        db.address.update(["ADDRESS_NAME", "COUNTRY", "CITY", "DISTRICT", "NEIGHBORHOOD", "AVENUE", "STREET", "ADDR_NUMBER", "ZIPCODE", "EXPLANATION"], values, "ADDRESS_ID", address_obj.address_id)

        flash("Address is updated successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    return render_template("address/address_form.html", form=form, address=address_obj, head_title="Edit address")



@login_required
def address_delete_page(address_id):
    db = current_app.config["db"]
    customer_id = db.customer_address.get_row("CUSTOMER_ID", "ADDRESS_ID", address_id)
    if current_user.id != customer_id and not current_user.is_admin:
        return abort(401)

    db.customer_address.delete(address_id)
    db.address.delete(address_id)
    return redirect(url_for("addresses_page"))
