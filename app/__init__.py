from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)

api = Api(app)
from app.urls import urls
for url, resource in urls.items():
    api.add_resource(resource, url)

db.init_app(app)
