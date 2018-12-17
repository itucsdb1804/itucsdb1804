from flask import Flask
from flask_login import LoginManager
from database import Database
from views import *


lm = LoginManager()
db = Database()


@lm.user_loader
def load_user(user_id):
    return db.customer.get_row("*", "CUSTOMER_ID", user_id)


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
    app.add_url_rule("/shopping-cart/tp-<int:transaction_id>-<int:book_id>-<int:edition_number>", view_func=transaction_view.tp_delete_page)

    app.add_url_rule("/customers", view_func=customer_view.customers_page)
    app.add_url_rule("/addresses", view_func=general_views.addresses_page)
    app.add_url_rule("/persons", view_func=general_views.persons_page)

    return app


app = create_app()

if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
