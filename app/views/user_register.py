from flask_restful import Resource

from app.models import UserModel
from utils.jsonschema_patterns import nonempty_string, email_type
from utils.validation_decorator import validate_request_json

SCHEMA = {
    "type": "object",
    "properties": {
        "username": nonempty_string,
        "password": nonempty_string,
        "email": email_type,
    },
    "required": ['username', 'password']
}


class UserRegister(Resource):
    @validate_request_json(SCHEMA)
    def post(self, json):
        if UserModel.find_by_username(json['username']):
            return {"error": {"username": "A user with that username already exist"}}, 400

        user = UserModel(username=json['username'])
        user.set_password(json['password'])
        if json.get('email'):
            user.email = json['email']
        user.save_to_db()

        return {"message": "User created successfully"}, 201
