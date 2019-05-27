from sys import exit

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

try:
    from config import DATABASE_CONNECTION
except ImportError:
    print("Не задана переменная DATABASE_CONNECTION")
    exit(1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
# Handle CORS
CORS(app)
# Init database
db = SQLAlchemy(app)
db.init_app(app)

# Init api methods
api = Api(app)
from app.urls import urls
for url, resource in urls.items():
    api.add_resource(resource, url)