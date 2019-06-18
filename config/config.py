import os
from dotenv import load_dotenv
from os.path import dirname, abspath

load_dotenv()
BASE_DIRECTORY = dirname(dirname(abspath(__file__)))


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY') or 'some-special-secret-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or "sqlite:///{}/data.db".format(BASE_DIRECTORY)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
