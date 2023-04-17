from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.models import User
from app.schemas import UserSchema
from app.services import UserService


user_service = UserService()


class UsersResource(Resource):
    def get(self):
        users = db.session.query(User).all()
        return jsonify(UserSchema().dump(users, many=True))

    def post(self):
        json_data = request.get_json()
        user = user_service.create(json_data)

        response = jsonify(UserSchema().dump(user, many=False))
        response.status_code = 201
        return response


class UserResource(Resource):
    def get(self, user_id):
        user = user_service.get_by_id(user_id)
        return jsonify(UserSchema().dump(user, many=False))
