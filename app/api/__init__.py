from flask import Blueprint
from flask_restful import Api
from .user import UserResource, UsersResource


bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(bp)


api.add_resource(UsersResource, '/users', endpoint="users_list")
api.add_resource(UserResource, '/users/<int:user_id>', endpoint="user_details")
