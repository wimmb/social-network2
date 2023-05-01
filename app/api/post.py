from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.models import Post, Like, Dislike
from app.schemas import PostSchema, LikeSchema, DislikeSchema
from app.services import PostService, LikeService, DislikeService


post_service = PostService()
like_service = LikeService()
dislike_service = DislikeService()


class PostsResource(Resource):
    def get(self):
        author_id = request.args.get('author_id', type=int)
        post_id = request.args.get('post_id', type=int)

        posts_query = db.session.query(Post)
        if author_id:
            posts_query = posts_query.filter(Post.author_id == author_id)

        if author_id and post_id:
            posts_query = posts_query.filter(
                Post.author_id == author_id,
                Post.id == post_id
            )
            post = posts_query.first()
            return jsonify(PostSchema().dump(post, many=False))

        posts = posts_query.all()
        return jsonify(PostSchema().dump(posts, many=True))

    def post(self):
        author_id = request.args.get('author_id', type=int)

        json_data = request.get_json()

        if author_id:
            json_data['author_id'] = author_id

        post = post_service.create(**json_data)

        response = jsonify(PostSchema().dump(post, many=False))
        response.status_code = 201
        return response


class PostResource(Resource):
    def get(self, post_id):
        post = post_service.get_by_id(post_id)
        return jsonify(PostSchema().dump(post, many=False))

    def put(self, post_id):
        json_data = request.get_json()
        json_data['id'] = post_id

        post = post_service.update(json_data)
        return jsonify(PostSchema().dump(post, many=False))

    def delete(self, post_id):
        status = post_service.delete(post_id)
        return jsonify(status=status)


class LikesResource(Resource):
    def get(self):
        like_id = request.args.get('like_id', type=int)

        likes_query = db.session.query(Like)
        if like_id:
            likes_query = likes_query.filter(Like.id == like_id)
            like = likes_query.first()
            return jsonify(LikeSchema().dump(like, many=False))

        likes = likes_query.all()
        return jsonify(LikeSchema().dump(likes, many=True))

    def post(self):
        json_data = request.get_json()

        post_id = json_data['post_id']
        user_id = json_data['user_id']

        like = (
            db.session.query(Like)
            .filter(
                Like.post_id == post_id,
                Like.user_id == user_id
            )
            .first()
        )

        if like:
            response = jsonify(error="Like already set")
            response.status_code = 400
            return response

        new_like = like_service.create(**json_data)

        response = jsonify(LikeSchema().dump(new_like, many=False))
        response.status_code = 201
        return response


class DislikesResource(Resource):
    def get(self):
        dislike_id = request.args.get('dislike_id', type=int)

        dislikes_query = db.session.query(Dislike)
        if dislike_id:
            dislikes_query = dislikes_query.filter(Dislike.id == dislike_id)
            dislike = dislikes_query.first()
            return jsonify(DislikeSchema().dump(dislike, many=False))

        dislikes = dislikes_query.all()
        return jsonify(DislikeSchema().dump(dislikes, many=True))

    def post(self):
        json_data = request.get_json()

        post_id = json_data['post_id']
        user_id = json_data['user_id']

        dislike = (
            db.session.query(Dislike)
            .filter(
                Dislike.post_id == post_id,
                Dislike.user_id == user_id
            )
            .first()
        )

        if dislike:
            response = jsonify(error="Dislike already set")
            response.status_code = 400
            return response

        new_dislike = dislike_service.create(**json_data)

        response = jsonify(DislikeSchema().dump(new_dislike, many=False))
        response.status_code = 201
        return response
