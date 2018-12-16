from flask import current_app, render_template, abort, request, redirect, url_for, flash
from tables import AuthorObj, PersonObj
from forms import AuthorForm


def authors_page():
    db = current_app.config["db"]
    authors = db.author.get_table()
    return render_template("author/authors.html", authors=authors)


def author_take_info_from_form(form):
    '''
    p_name = form.data["p_name"]
    p_surname = form.data["p_surname"]
    p_gender = form.data["p_gender"]
    p_dob = form.data["p_dob"]
    p_nationality = form.data["p_nationality"]
    a_biography = form.data["author_biography"]
    '''
    return ([form.data["p_name"], form.data["p_surname"], form.data["p_gender"], form.data["p_dob"], form.data["p_nationality"]], form.data["author_biography"])


def add_author(name=None):
    db = current_app.config["db"]
    form = AuthorForm()
    if form.validate_on_submit():
        values = author_take_info_from_form(form)

        person_id = db.person.add(*values[0])
        db.author.add(person_id, values[1])
        
        flash("Author is added successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)

    return render_template("author/author_add.html", form=form)



def author_edit_page(author_id):
    db = current_app.config["db"]
    form = AuthorForm()
    author_obj = db.author.get_row("*", "AUTHOR_ID", author_id)
    person_obj = db.person.get_row("*", "PERSON_ID", author_obj.person_id)
    if form.validate_on_submit():
        values = author_take_info_from_form(form)
        db.person.update(["PERSON_NAME", "SURNAME", "GENDER", "DATE_OF_BIRTH", "NATIONALITY"], values[0], "PERSON_ID", author_obj.person_id)
        db.author.update("BIOGRAPHY", values[1], "AUTHOR_ID", author_id)

        flash("Author is updated successfully", "success")
        next_page = request.args.get("next", url_for("home_page"))
        return redirect(next_page)
    
    return render_template("author/author_edit.html", form=form, person=person_obj, author=author_obj)



def author_delete_page(author_id):
    db = current_app.config["db"]
    db.author.delete(author_id)
    return redirect(url_for("authors_page"))