from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.models import Post
from app.schemas import PostSchema
from app.services import PostService


post_service = PostService()


class PostsResource(Resource):
    def get(self):
        ordered = request.args.get('ordered', type=bool)

        posts_query = db.session.query(Post)
        if ordered:
            posts_query = posts_query.order_by(Post.created_at.asc())

        posts = posts_query.all()
        return jsonify(PostSchema().dump(posts, many=True))

    def post(self):
        json_data = request.get_json()
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
