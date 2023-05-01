from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.models import User, Profile
from app.schemas import UserSchema, ProfileSchema
from app.services import UserService, ProfileService


user_service = UserService()
profile_service = ProfileService()


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


class ProfilesResource(Resource):

    def get(self):
        profile_id = request.args.get('profile_id', type=int)
        user_id = request.args.get('user_id', type=int)

        profiles_query = db.session.query(Profile)

        if profile_id:
            profiles_query = profiles_query.filter(Profile.id == profile_id)
            profile = profiles_query.first()
            return jsonify(ProfileSchema().dump(profile, many=False))

        if user_id:
            profiles_query = profiles_query.filter(Profile.user_id == user_id)
            profile = profiles_query.first()
            return jsonify(ProfileSchema().dump(profile, many=False))

        profiles = profiles_query.all()
        return jsonify(ProfileSchema().dump(profiles, many=True))

    def put(self):
        profile_id = request.args.get('profile_id', type=int)
        # user_id = request.args.get('user_id', type=int)

        json_data = request.get_json()

        if profile_id:
            json_data['id'] = profile_id
            profile = profile_service.update(json_data)
            return jsonify(ProfileSchema().dump(profile, many=False))

        # if user_id:
        #     json_data['user_id'] = user_id
        #     profile = profile_service.update(json_data)
        #     return jsonify(ProfileSchema().dump(profile, many=False))

        response = jsonify(error="Profile not found")
        response.status_code = 400
        return response
