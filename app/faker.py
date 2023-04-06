import click
from flask import Blueprint
from faker import Faker

from app import db
from app.models import User, Profile
from werkzeug.security import generate_password_hash

bp = Blueprint('fake', __name__)
faker = Faker()


@bp.cli.command("users")
@click.argument('num', type=int)
def users(num):

    for i in range(num):
        # generate fake username
        username = faker.user_name()

        # generate fake email
        email = faker.email()

        # generate fake password
        password_no_hash = faker.password()
        password = generate_password_hash(password_no_hash)

        # generate fake first_name
        first_name = faker.first_name()

        # generate fake last_name
        last_name = faker.last_name()

        # generate fake linkedin_url
        linkedin_url = f'https://linkedin.com/{username}'

        # generate fake facebook_url
        facebook_url = f'https://facebook.com/{username}'

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
                password=password
            )
            db.session.add(user)
            db.session.commit()

            profile = Profile(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                linkedin_url=linkedin_url,
                facebook_url=facebook_url
            )

            db.session.add(profile)
            db.session.commit()

        print(username, password_no_hash)

    print(num, 'users added.')
