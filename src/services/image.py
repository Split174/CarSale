import uuid
import os
from flask import (
    current_app,
    url_for,
    send_from_directory
)


class ImageService:
    def __init__(self, connection):
        self.connection = connection

    def save_file(self, file):
        """
        Сохранить файл на сервер
        :param file:
        :return:
        """
        upload_dir = current_app.config['UPLOAD_DIR']
        filename = f'{uuid.uuid4()}{os.path.splitext(file.filename)[1]}' # TODO проверять типы файлов
        print(filename)
        file.save(os.path.join(upload_dir, filename[:-1])) # magic slice
        return {
            'url': url_for('images.download_image', image_name=filename, _external=True)
        }

    def get_image(self, image_name):
        """
        Получить файл с сервера
        """
        upload_dir = current_app.config['UPLOAD_DIR']
        return send_from_directory(upload_dir, image_name)