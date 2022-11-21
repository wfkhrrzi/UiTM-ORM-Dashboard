"""Flask configuration."""
from os import path,environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

APP_DEBUG = bool(environ.get('APP_DEBUG'))
BERTOPIC_HOST = environ.get('BERTOPIC_HOST')
SENTIMENT_HOST = environ.get('SENTIMENT_HOST')

DB_NAME = environ.get('DB_NAME')