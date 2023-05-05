from flask import Blueprint
from sqlalchemy import func
from pathlib import Path
import pandas as pd
import config

from .. import db
from ..models import User, Profile, Post

bp = Blueprint("user", __name__, url_prefix="/user")
from . import routes # noqa


@bp.cli.command('extract_users')
def extract_users():
    users_info = (
        db.session.query(User.username, User.email, Profile.full_name, func.count('*'))
        .join(Profile, Profile.user_id == User.id)
        .join(Post, Post.author_id == User.id)
        .group_by(User.username, User.email, Profile.full_name)
        .all()
    )

    df = pd.DataFrame(users_info, columns=['Username', 'Email', 'Full Name', 'Post Count'])

    output_file_path = Path(config.basedir) / 'users.csv'
    df.to_csv(output_file_path)

    print('Users info saved to users.csv')
