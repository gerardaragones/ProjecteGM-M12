"""Flask APP configuration."""
from os import environ, path
from dotenv import load_dotenv


# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir + "/" + environ.get('SQLITE_FILE_RELATIVE_PATH')
    RUTA_FOTOS = environ.get('RUTA_FOTOS')