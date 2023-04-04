import click
from flask import Blueprint
from faker import Faker

from app import db
from app.models import User


bp = Blueprint('fake', __name__)
faker = Faker()


@bp.cli.command("users")
@click.argument('num', type=int)
def users(num):
    users = []
    for i in range(num):
        # generate fake username
        username = faker.user_name()

        # generate fake email
        email = faker.email()

        # generate fake password
        password = faker.password()

        # get user by username & email
        user = (
            db.session.query(User)
            .filter(
                User.username == username,
                User.email == email,
                User.password is not None
            )
        ).first()

        # no such user in db yet --> insert
        if not user:
            user = User(
                username=username,
                email=email,
                password=password,
            )
            db.session.add(user)
            users.append(user)

    # persist changes
    db.session.commit()
    print(num, 'users added.')
