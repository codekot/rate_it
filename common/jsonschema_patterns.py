#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит паттерны для использования в валидации с помощью jsonschema
"""

from __future__ import unicode_literals

from jsonschema import Draft4Validator, FormatChecker


def validate(data, scheme):
    validator = Draft4Validator(scheme, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    path_errors = {}
    simple_errors = []
    for error in iter(errors):
        error_path = '.'.join(str(path) for path in error.absolute_path)
        message = error.message.replace(r"u'", "'")
        if error_path:
            path_errors[error_path] = message
        else:
            simple_errors.append(message)
    if simple_errors and path_errors:
        simple_errors.append(path_errors)
        return simple_errors
    elif simple_errors:
        return simple_errors
    return path_errors


nonempty_string = {
    "type": "string",
    'minLength': 1,
}

email_type = {
    'type': 'string',
    'minLength': 1,
    'pattern': '^.+@.+\..+$',
}
