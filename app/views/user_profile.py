from flask_restful import Resource

from app.models import UserModel
from utils.identify_user import identify_user
from utils.jsonschema_patterns import nonempty_string, email_type
from utils.jwt_required import jwt_required
from utils.validation_decorator import validate_request_json

PUT_SCHEMA = {
    "type": "object",
    "properties": {
        "username": nonempty_string,
        "password": nonempty_string,
        "new_password": nonempty_string,
        "email": email_type,
        "item_view": {'enum': [value for name, value in UserModel.ITEM_VIEWS]},
    },
}


class UserProfile(Resource):

    @jwt_required
    @identify_user
    def get(self, current_user):
        return {
            'username': current_user.username,
            'email': current_user.email,
            'item_view': current_user.item_view.value,
        }

    @jwt_required
    @identify_user
    @validate_request_json(PUT_SCHEMA)
    def put(self, current_user, json):
        if json.get("new_password") and not json.get("password"):
            return {"errors": ["To change password please provide old password."]}, 400
        elif json.get("new_password") and not current_user.check_password(json["password"]):
            return {"errors": ["Provided password is incorrect."]}, 400

        if json.get("new_password"):
            current_user.set_password(json["new_password"])
        for field in 'username,email,item_view'.split(','):
            if field not in json:
                continue
            setattr(current_user, field, json[field])
        current_user.save_to_db()

        return {}, 200
