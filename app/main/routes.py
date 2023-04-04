from app import db
from app.main import bp
from flask import render_template

from app.models import User


@bp.route("/")
@bp.route("/index")
def index():

    users_data = [
        {
            "username": "user11",
            "email": "user11@gmail.com",
            "password": "user11"
        },
        {
            "username": "user22",
            "email": "user22@gmail.com",
            "password": "user22"
        },
        {
            "username": "user33",
            "email": "user33@gmail.com",
            "password": "user33"
        },
    ]

    for u in users_data:
        user = (
            db.session.query(User)
            .filter(
                User.username == u.get('username'),
                User.email == u.get('email'),
                User.password == u.get('password')
            ).first()
        )
        if user:
            continue

        user = User(
            username=u.get('username'),
            email=u.get('email'),
            password=u.get('password')
        )
        db.session.add(user)
    db.session.commit()

    users = db.session.query(User).all()

    context = {
        "title": "Home page",
        "users": users
    }
    return render_template("index.html", **context)


@bp.route("/about")
def about():
    return render_template("about.html")

