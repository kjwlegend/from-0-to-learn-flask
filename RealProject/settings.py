from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = 'dev'

SQLALCHEMY_DATABASE_URI = 'mysql://learflask:learflask@localhost:3306/learflask?charset=utf8'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True