from app import db
from app.models import User, Profile, Post, Like, Dislike
from app.schemas import UserSchema, PostSchema, ProfileSchema


class UserService:

    def get_by_id(self, user_id):
        user = db.session.query(User).filter(User.id == user_id).first_or_404()
        return user

    def get_by_username(self, username):
        user = db.session.query(User).filter(User.username == username).first_or_404()
        return user

    def create(self, **kwargs):
        user = User(username=kwargs.get('username'), email=kwargs.get('email'))
        user.set_password(kwargs.get('password'))

        db.session.add(user)
        db.session.commit()

        profile = Profile(
            user_id=user.id,
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            linkedin_url=kwargs.get('linkedin_url'),
            facebook_url=kwargs.get('facebook_url')
        )
        db.session.add(profile)
        db.session.commit()

        return user

    def update(self, data):
        user = self.get_by_id(data['id'])
        data['profile']['id'] = user.profile.id
        data['profile']['user_id'] = user.id

        user = UserSchema().load(data)
        db.session.add(user)
        db.session.commit()

        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        profile = user.profile
        db.session.delete(profile)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        return True


class PostService:

    def get_by_id(self, post_id):
        post = db.session.query(Post).filter(Post.id == post_id).first_or_404()
        return post

    def create(self, **kwargs):
        post = Post(title=kwargs.get('title'), content=kwargs.get('content'), author_id=kwargs.get('author_id'))
        db.session.add(post)
        db.session.commit()
        return post

    def update(self, data):
        post = self.get_by_id(data['id'])
        data['author_id'] = post.author_id

        post_dict = PostSchema().dump(post)
        post_dict.update(data)

        post = PostSchema().load(post_dict)
        db.session.add(post)
        db.session.commit()

        return post

    def delete(self, post_id):
        post = self.get_by_id(post_id)

        db.session.delete(post)
        db.session.commit()

        return True


class ProfileService:

    def get_by_id(self, profile_id):
        profile = db.session.query(Profile).filter(Profile.id == profile_id).first_or_404()
        return profile

    def update(self, data):
        profile = self.get_by_id(data['id'])
        data['id'] = profile.id
        data['user_id'] = profile.user_id

        profile = ProfileSchema().load(data)
        db.session.add(profile)
        db.session.commit()

        return profile


class LikeService:
    def create(self, **kwargs):
        like_post = Like(user_id=kwargs.get('user_id'), post_id=kwargs.get('post_id'))
        db.session.add(like_post)
        db.session.commit()
        return like_post


class DislikeService:
    def create(self, **kwargs):
        dislike_post = Dislike(user_id=kwargs.get('user_id'), post_id=kwargs.get('post_id'))
        db.session.add(dislike_post)
        db.session.commit()
        return dislike_post