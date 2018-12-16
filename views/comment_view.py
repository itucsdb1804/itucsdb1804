from flask import current_app, abort, request, render_template, redirect, url_for
from table_operations.control import Control
from flask_login import current_user, login_required


def comments_page():
    comments = take_comments_with_and_by(with_book=True)
    return render_template("comments.html", comments=comments)


# # TODO giriş gerekli
# @login_required
def comment_edit_page(comment_id):
    db = current_app.config["db"]

    # Take comment information and if there is no comment with comment id, abort 404 page
    comment = db.comment.get_row(comment_id)
    if comment is None:
        abort(404)

    # # TODO Yorumu yapanın id'si ile şimdiki kullanıcının id'si aynı değilse?
    # if comment.customer_id != current_user.id:
    #     abort(401)

    if request.method == "GET":
        values = {"comment_title": comment.comment_title, "comment_statement": comment.comment_statement, "rating": comment.rating}
        return render_template("comment/comment_form.html", title="Comment editing", comment_values=values)
    else:
        values = {"customer_id": comment.customer_id, "book_id": comment.book_id, "comment_title": request.form["comment_title"], "comment_statement": request.form["comment_statement"], "rating": request.form["rating"]}

        # Invalid input control
        err_message = Control().Input().comment(values)
        if err_message:
            return render_template("book/book.html", title="Comment editing", comment_values=values, err_message=err_message)

        # Update comment variable
        comment.comment_title = values["comment_title"]
        comment.comment_statement = values["comment_statement"]
        comment.rating = values["rating"]
        # Update comment in database
        db.comment.update(comment.comment_id, comment)

        return redirect(url_for("book_page", book_key=comment.book_id))


def comment_delete_page(comment_id):
    db = current_app.config["db"]

    comment = db.comment.get_row(comment_id)
    if comment is None:
        abort(401)

    db.comment.delete(comment_id)
    return redirect(url_for("book_page", book_key=comment.book_id))


def take_comments_with_and_by(book_id=None, with_book=False):
    db = current_app.config["db"]
    comments = []
    if with_book:
        for comment in db.comment.get_table(book_id=book_id):
            comments.append((comment, db.customer.get_row(where_columns="CUSTOMER_ID", where_values=comment.customer_id), db.book.get_row(comment.book_id)))
    else:
        for comment in db.comment.get_table(book_id=book_id):
            comments.append((comment, db.customer.get_row(where_columns="CUSTOMER_ID", where_values=comment.customer_id)))

    return comments
