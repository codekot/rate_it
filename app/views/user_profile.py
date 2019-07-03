from flask_restful import Resource

from utils.identify_user import identify_user
from utils.jwt_required import jwt_required


class UserProfile(Resource):

    @jwt_required
    @identify_user
    def get(self, current_user):
        return {
            'username': current_user.username,
            'email': current_user.email,
            'item_view': current_user.item_view.value,
        }
