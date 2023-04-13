from datetime import datetime
from hashlib import md5

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class User(BaseModel, UserMixin):
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship(
        "Post", backref="author", uselist=True, lazy="dynamic", cascade="all,delete"
    )
    likes = db.relationship(
        'Like', backref='user', lazy='dynamic', primaryjoin='User.id==Like.user_id', cascade="all,delete"
    )
    dislikes = db.relationship(
        'Dislike', backref='user', lazy='dynamic', primaryjoin='User.id==Dislike.user_id', cascade="all,delete"
    )
    # list of users that follow you
    followers = db.relationship("Follow", backref="followee", foreign_keys="Follow.followee_id")
    # list of users that you follow
    following = db.relationship("Follow", backref="follower", foreign_keys="Follow.follower_id")

    def is_following(self, current_user_id):
        follower = (
            db.session.query(Follow)
            .filter(
                db.and_(
                    Follow.follower_id == self.id,
                    Follow.followee_id == current_user_id
                )
            )
            .first()
        )
        return follower is not None

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.username} ({self.email})"


class Profile(BaseModel):
    __tablename__ = "profiles"
    __table_args__ = (
        db.Index("idx_profiles_user_id", "user_id"),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_profiles_user_id", ondelete="CASCADE"),
        nullable=False
    )

    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    linkedin_url = db.Column(db.String, nullable=True)
    facebook_url = db.Column(db.String, nullable=True)
    bio = db.Column(db.String)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("profile", uselist=False), uselist=False)


class Post(BaseModel):
    __tablename__ = "posts"

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_posts_author_id", ondelete="CASCADE"),
        nullable=False
    )
    likes = db.relationship("Like", backref="post", uselist=True, cascade="all,delete")
    dislikes = db.relationship("Dislike", backref="post", uselist=True, cascade="all,delete")


class Like(BaseModel):
    __tablename__ = "likes"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_likes_user_id"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', name="fk_likes_post_id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Dislike(BaseModel):
    __tablename__ = "dislikes"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_dislikes_user_id"),
        nullable=False
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', name="fk_dislikes_post_id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Follow(db.Model):
    __tablename__ = 'follows'

    follower_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_follows_follower_id"),
        primary_key=True
    )
    followee_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name="fk_follows_followee_id"),
        primary_key=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
