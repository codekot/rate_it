#!/usr/bin/env python
from app import app
try:
    from config import DEBUG, HOST, PORT
except:
    DEBUG = None
    HOST = None
    DEBUG = None


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
    app.url_map.strict_slashes = False
