from app.user import bp
from flask import render_template, redirect, url_for
from flask_login import current_user

from .. import db
from ..models import User


@bp.route("/profile/<string:username>")
def profile(username):
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = db.session.query(User).filter(User.username == username).first_or_404()
    context = {
        "title": f"{user.username} - profile",
        "user": user
    }

    return render_template("user/profile.html", **context)
