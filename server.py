from flask import Flask
import datetime
import views


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/books", view_func=views.books_page)
    app.add_url_rule("/stores", view_func=views.stores_page)
    app.add_url_rule("/comments", view_func=views.comments_page)
    app.add_url_rule("/customers", view_func=views.customers_page)
    app.add_url_rule("/addresses", view_func=views.addresses_page)
    app.add_url_rule("/persons", view_func=views.persons_page)
    app.add_url_rule("/books_edit", view_func=views.movie_add_page)

    return app


app = create_app()

if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run()
