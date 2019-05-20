"""Для старта работы скопируйте этот модуль в config/config.py и задайте нужные параметры подключения."""

from os.path import dirname, abspath

BASE_DIRECTORY = dirname(dirname(abspath(__file__)))
DATABASE_CONNECTION = f"sqlite:///{BASE_DIRECTORY}/data.db"
DEBUG = False
