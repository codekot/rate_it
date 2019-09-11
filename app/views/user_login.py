from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from app.models import UserModel


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username field is required")
        parser.add_argument('password', type=str, required=True, help="Password field is required")
        args = parser.parse_args()

        # Get user
        user = UserModel.find_by_username(args["username"])
        if not user:
            return {"errors": {"username": "Invalid username"}}, 400

        # Check password
        if not user.check_password(args["password"]):
            return {"errors": {"password": "Invalid password"}}, 400

        # Create token
        access_token = create_access_token(identity=user.id, expires_delta=False, fresh=True)
        return {
            'access_token': access_token,
            'user': {
                'username': user.username,
                'email': user.email,
                'item_view': user.item_view.value,
            }
        }, 200
