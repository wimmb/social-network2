from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.models import User
from app.schemas import UserSchema
from app.services import UserService


user_service = UserService()


class UsersResource(Resource):
    def get(self):
        ordered = request.args.get('ordered', type=bool)

        users_query = db.session.query(User)
        if ordered:
            users_query = users_query.order_by(User.created_at.asc())

        users = users_query.all()
        return jsonify(UserSchema().dump(users, many=True))

    def post(self):
        json_data = request.get_json()
        user = user_service.create(**json_data)

        response = jsonify(UserSchema().dump(user, many=False))
        response.status_code = 201
        return response


class UserResource(Resource):
    def get(self, user_id):
        user = user_service.get_by_id(user_id)
        return jsonify(UserSchema().dump(user, many=False))

    def put(self, user_id):
        json_data = request.get_json()
        json_data['id'] = user_id

        user = user_service.update(json_data)
        return jsonify(UserSchema().dump(user, many=False))

    def delete(self, user_id):
        status = user_service.delete(user_id)
        return jsonify(status=status)
