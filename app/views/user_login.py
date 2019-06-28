from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from app.models import UserModel


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username field is required")
        parser.add_argument('password', type=str, required=True, help="Password field is required")
        args = parser.parse_args()

        user = UserModel.find_by_username(args["username"])

        if user and user.check_password(args["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token': access_token}, 200
        elif user:
            return {"error": {"password": "Invalid password"}}, 400

        return {"error": {"username": "Invalid username"}}, 400
