from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

cors = CORS()
jwt = JWTManager()
db = SQLAlchemy()
api = Api()
migrate = Migrate()

# Init api methods
from app.urls import urls
for url, resource in urls.items():
    api.add_resource(resource, url)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Use strict slashes
    app.url_map.strict_slashes = False
    app.config["JWT_SECRET_KEY"] = "secret-key"

    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)

    return app
