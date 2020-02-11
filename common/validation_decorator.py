# coding=utf-8

import logging
from functools import wraps
from flask import request

from common.jsonschema_patterns import validate

logger = logging.getLogger()


def validate_request_json(schema):
    """Request JSON validation decorator"""
    def decorator(f):
        f.gw_method = f.__name__

        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                logger.error("No request JSON found for {}.".format(f.__name__))
                return {"errors": ["Invalid JSON format"]}, 400

            json = request.json
            errors = validate(json, schema)
            if errors:
                logger.error("Errors found during validation of {}: {}".format(f.__name__, errors))
                return {'errors': errors}, 400
            logger.debug('Validation for method {} completed, no errors'.format(f.__name__))

            kwargs['json'] = json
            return f(*args, **kwargs)

        return wrapper
    return decorator
