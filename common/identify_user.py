# coding=utf-8

import logging
from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.models import UserModel

logger = logging.getLogger()


def identify_user(f):
    f.gw_method = f.__name__

    @wraps(f)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        current_user = UserModel.find_by_id(current_user)
        if not current_user:
            return {"errors": ["Token is correct but there is no user with this id"]}, 401
        kwargs['current_user'] = current_user
        return f(*args, **kwargs)

    return wrapper
