from app import db
from app.main import bp
from flask import render_template

from app.models import User


@bp.route("/")
@bp.route("/index")
def index():
    users = db.session.query(User).all()
    context = {
        "title": "Social Network",
        "users": users
    }
    return render_template("index.html", **context)


@bp.route("/about")
def about():
    return render_template("about.html")
