from flask import Flask
from flask_login import LoginManager
from database import Database
import views


lm = LoginManager()
db = Database()

@lm.user_loader
def load_user(user_id):
    return db.customer.get_row("CUSTOMER_ID", user_id)


def create_app():

    app = Flask(__name__)
    app.config.from_object("settings")
    app.config["db"] = db

    lm.init_app(app)
    lm.login_view = views.login_page

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/signup", view_func=views.signup_page, methods=["GET", "POST"])
    app.add_url_rule("/books", view_func=views.books_page, methods=["GET", "POST"])
    app.add_url_rule("/books/add-new", view_func=views.book_add_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_key>", view_func=views.book_page)
    app.add_url_rule("/books/<int:book_key>/edit", view_func=views.book_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_key>/delete", view_func=views.book_delete_page)
    app.add_url_rule("/stores", view_func=views.stores_page)
    app.add_url_rule("/comments", view_func=views.comments_page)
    app.add_url_rule("/customers", view_func=views.customers_page)
    app.add_url_rule("/addresses", view_func=views.addresses_page)
    app.add_url_rule("/persons", view_func=views.persons_page)
    app.add_url_rule("/products", view_func=views.products_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_id>/<int:edition_number>", view_func=views.book_edition_page)
    app.add_url_rule("/books/add-edition", view_func=views.book_edition_add_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_id>/<int:edition_number>/edit", view_func=views.book_edition_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_id>/<int:edition_number>/delete", view_func=views.book_edition_delete_page, methods=["GET", "POST"])

    return app


app = create_app()

if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
