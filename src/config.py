import os


class Config:
    """
    Класс конфигов для flas_app
    """
    DB_CONNECTION = os.getenv('DB_CONNECTION', 'db.sqlite')
    SECRET_KEY = os.getenv('SECRET_KEY')
    IMG_FOLDER = os.path.join(os.getcwd(), 'images')