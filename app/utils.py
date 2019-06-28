def non_empty_string(string):
    """None empty string type for RequestParser"""
    if not isinstance(string, str):
        raise ValueError("Must be string")
    if not string:
        raise ValueError("Must be non-empty string")
    return string
