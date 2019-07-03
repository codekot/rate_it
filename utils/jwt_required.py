# coding=utf-8

import logging
from functools import wraps

from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from jwt.exceptions import ExpiredSignatureError, DecodeError

logger = logging.getLogger()


def jwt_required(f):
    """Request JWT Authorization decorator"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except ExpiredSignatureError as exc:
            return {'errors': ["Authentication token has expired"]}, 401
        except (InvalidHeaderError, DecodeError) as exc:
            return {'errors': ["Invalid token"]}, 401
        except NoAuthorizationError as exc:
            return {'errors': ["No token provided"]}, 401

        return f(*args, **kwargs)

    return wrapper
