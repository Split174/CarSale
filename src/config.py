import os


class Config:
    """
    Класс конфигов для flask_app
    """
    DB_CONNECTION = os.getenv('DB_CONNECTION', 'db.sqlite')
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))

