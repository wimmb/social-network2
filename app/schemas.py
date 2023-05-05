from marshmallow import EXCLUDE, fields
from marshmallow.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchemaOpts, SQLAlchemyAutoSchema
from app import db
from app.models import User, Profile, Post, Like, Dislike
from marshmallow.decorators import post_dump


class BaseOpts(SQLAlchemyAutoSchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = db.session
        if not hasattr(meta, "unknown"):
            meta.unknown = EXCLUDE
        if not hasattr(meta, "load_instance"):
            meta.load_instance = True
        if not hasattr(meta, "include_fk"):
            meta.include_fk = True
        super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemyAutoSchema):
    OPTIONS_CLASS = BaseOpts


class ProfileSchema(BaseSchema):
    class Meta:
        model = Profile

    # full_name = fields.String(dump_only=True)


class LikeSchema(BaseSchema):
    class Meta:
        model = Like

    post_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)


class DislikeSchema(BaseSchema):
    class Meta:
        model = Dislike

    post_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)


class PostSchema(BaseSchema):
    class Meta:
        model = Post

    likes = Nested(LikeSchema(), many=True, dump_only=True)
    dislikes = Nested(DislikeSchema(), many=True, dump_only=True)

    @post_dump(pass_many=False)
    def add_like_count(self, data, **kwargs):
        data['like_count'] = len(data['likes'])
        del data['likes']
        return data

    @post_dump(pass_many=False)
    def add_dislike_count(self, data, **kwargs):
        data['dislike_count'] = len(data['dislikes'])
        del data['dislikes']
        return data


class UserSchema(BaseSchema):
    class Meta:
        model = User
        exclude = ('password',)

    profile = Nested(ProfileSchema(), many=False)
    posts = Nested(PostSchema(), many=True, dump_only=True)

    @post_dump(pass_many=False)
    def add_post_count(self, data, **kwargs):
        data['post_count'] = len(data['posts'])
        del data['posts']
        return data
