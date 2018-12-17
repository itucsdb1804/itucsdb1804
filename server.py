from flask import Flask, abort, render_template
from flask_login import LoginManager
from database import Database
from views import *


lm = LoginManager()
db = Database()


@lm.user_loader
def load_user(user_id):
    return db.customer.get_row("*", "CUSTOMER_ID", user_id)

@lm.unauthorized_handler
def unauthorized_access():
    return abort(401)


def create_app():

    app = Flask(__name__)
    app.config.from_object("settings")
    app.config["db"] = db

    lm.init_app(app)
    lm.login_view = login_view.login_page

    app.add_url_rule("/", view_func=general_views.home_page)
    app.add_url_rule("/login", view_func=login_view.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=login_view.logout_page)
    app.add_url_rule("/signup", view_func=login_view.signup_page, methods=["GET", "POST"])

    # Book pages
    app.add_url_rule("/books", view_func=book_view.books_page, methods=["GET", "POST"])
    app.add_url_rule("/books/add-new", view_func=book_view.book_add_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_key>", view_func=book_view.book_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_key>/edit", view_func=book_view.book_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_key>/delete", view_func=book_view.book_delete_page)

    # Book Edition pages
    app.add_url_rule("/books/add-edition", view_func=book_edition_view.book_edition_add_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_id>/<int:edition_number>", view_func=book_edition_view.book_edition_page)
    app.add_url_rule("/books/<int:book_id>/<int:edition_number>/edit", view_func=book_edition_view.book_edition_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_id>/<int:edition_number>/delete", view_func=book_edition_view.book_edition_delete_page, methods=["GET", "POST"])

    # Product pages
    app.add_url_rule("/products", view_func=product_view.products_page, methods=["GET", "POST"])
    app.add_url_rule("/products/add-new", view_func=product_view.product_add_page, methods=["GET", "POST"])
    app.add_url_rule("/products/<int:book_id>/<int:edition_number>", view_func=product_view.product_page, methods=["GET", "POST"])
    app.add_url_rule("/products/<int:book_id>/<int:edition_number>/edit", view_func=product_view.product_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/products/<int:book_id>/<int:edition_number>/delete", view_func=product_view.product_delete_page, methods=["GET", "POST"])

    # Comment pages
    app.add_url_rule("/comments", view_func=comment_view.comments_page)
    app.add_url_rule("/comments/<int:comment_id>/edit", view_func=comment_view.comment_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/comments/<int:comment_id>/delete", view_func=comment_view.comment_delete_page)

    # Transaction (Shopping Cart)
    app.add_url_rule("/shopping-cart", view_func=transaction_view.transaction_page)
    app.add_url_rule("/shopping-cart/next", view_func=transaction_view.transaction_next_page, methods=["GET", "POST"])
    app.add_url_rule("/shopping-cart/tp-<int:transaction_id>-<int:book_id>-<int:edition_number>/delete", view_func=transaction_view.tp_delete_page)

    # Address
    app.add_url_rule("/addresses", view_func=address_view.addresses_page)
    app.add_url_rule("/addresses/add-new", view_func=address_view.add_address, methods=["GET", "POST"])
    app.add_url_rule("/addresses/<int:address_id>/edit", view_func=address_view.address_edit_page, methods=["GET", "POST"])

    # Author
    app.add_url_rule("/authors", view_func=author_view.authors_page)
    app.add_url_rule("/authors/add-new", view_func=author_view.add_author, methods=["GET", "POST"])
    app.add_url_rule("/authors/<int:author_id>/edit", view_func=author_view.author_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/authors/<int:author_id>/books", view_func=author_view.books_by_author_page, methods=["GET", "POST"])

    # Category
    app.add_url_rule("/categories", view_func=category_view.categories_page)
    app.add_url_rule("/categories/<int:category_id>/books", view_func=category_view.books_by_category_page, methods=["GET", "POST"])

    # Customer
    app.add_url_rule("/customers", view_func=customer_view.customers_page)
    app.add_url_rule("/customers/<int:customer_id>/edit", view_func=customer_view.edit_customer_page, methods=["GET", "POST"])

    return app


app = create_app()

@app.errorhandler(401)
def unauthorized_access_page(err):
    return render_template("error/401.html")

@app.errorhandler(403)
def access_denied_page(err):
    return render_template("error/403.html")

@app.errorhandler(404)
def page_not_found(err):
    return render_template("error/404.html")



if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
