from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# MAIN PAGE
@app.route("/")
def index():
    return render_template("sign-up.html")


# SIGNUP
@app.route("/signup", methods=["POST"])
def signup():

    username = request.form.get("username")
    password = request.form.get("password")

    existing_user = User.query.filter_by(
        username=username
    ).first()

    if existing_user:
        return "User already exists."

    new_user = User(
        username=username,
        password=password
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("home"))


# LOGIN
@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(
        username=username,
        password=password
    ).first()

    if user:
        return redirect(url_for("home"))

    return "Invalid username or password."


# HOME PAGE
@app.route("/home")
def home():
    return render_template("home.html")


# LOGOUT
@app.route("/logout")
def logout():
    return redirect(url_for("index"))

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )