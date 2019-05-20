from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import DATABASE_CONNECTION

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
db = SQLAlchemy(app)

api = Api(app)
from app.urls import urls
for url, resource in urls.items():
    api.add_resource(resource, url)

db.init_app(app)
