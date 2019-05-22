from app import app
from config import DEBUG, HOST, PORT


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
    app.url_map.strict_slashes = False
