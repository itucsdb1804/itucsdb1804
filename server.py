from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/books")
def books_page():
    return render_template("books.html")


if __name__ == "__main__":
    app.run()