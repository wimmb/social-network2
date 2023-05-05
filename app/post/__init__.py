import click
from flask import Blueprint
from sqlalchemy import func
from pathlib import Path
import pandas as pd
import config

from .. import db
from ..models import User, Post, Like, Dislike

bp = Blueprint('post', __name__, url_prefix='/post')
from . import routes # noqa


@bp.cli.command('extract_posts')
@click.argument('user_id', type=int)
def extract_posts(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        print(f"User with id={user_id} not found!")
        return

    user_posts = (
        db.session.query(Post.title, func.count('*'), func.count('*'), Post.created_at)
        .join(Like, Post.id == Like.post_id)
        .join(Dislike, Post.id == Dislike.post_id)
        .group_by(Post.title, Post.created_at)
        .filter(Post.author_id == user_id)
        .all()
    )

    df = pd.DataFrame(user_posts, columns=['Post title', 'Likes', 'Dislikes', 'Created at'])

    output_file_path = Path(config.basedir) / f'{user.username.lower()}_posts.csv'
    df.to_csv(output_file_path)

    print(f"{user.username.title()}'s posts info saved to {user.username.lower()}_posts.csv")
