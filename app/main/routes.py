from app import db
from app.main import bp
from flask import render_template

from app.models import User, Post


@bp.route("/")
@bp.route("/index")
def index():
    posts = db.session.query(Post).order_by(Post.created_at.desc()).all()
    users = db.session.query(User).all()
    context = {
        "title": "Social Network",
        "users": users,
        "posts": posts
    }
    return render_template("index.html", **context)


@bp.route("/about")
def about():
    return render_template("about.html")
