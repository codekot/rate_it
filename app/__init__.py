from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from config import Config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

cors = CORS()
jwt = JWTManager()
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
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
    migrate.init_app(app, db, render_as_batch=True)

    return app
