from flask_restful import Resource, reqparse

from app.models import UserModel
from app.utils import non_empty_string


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=non_empty_string, required=True, help="Username field is required")
        parser.add_argument('password', type=str, required=True, help="Password field is required")
        parser.add_argument('email', type=str, help="Email is used for password reset only")
        args = parser.parse_args()

        if UserModel.find_by_username(args['username']):
            return {"error": {"username": "A user with that username already exist"}}, 400

        user = UserModel(username=args['username'])
        user.set_password(args['password'])
        user.save_to_db()

        return {"message": "User created successfully"}, 201
