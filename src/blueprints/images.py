from flask import (
    Blueprint,
    jsonify,
    request,
    session,
)
from flask.views import MethodView
from services.image import ImageService
from services.user import  UserService
from database import db


class ImagesView(MethodView):
    def post(self):
        """
        Загрузить изображение на сервер
        """
        if session.get('user_id') is None:
            return '', 401
        user_service = UserService(db.connection)
        if not user_service.is_user_a_seller(session.get('user_id')):
            return 'загружать фотографии могут только продавцы', 403

        file = request.files['image']
        image_service = ImageService(db.connection)
        url = image_service.save_file(file)
        return jsonify(url), 201


class ImageView(MethodView):
    def get(self, image_name):
        """
        Получить изображение
        """
        image_service = ImageService(db.connection)
        return image_service.get_image(image_name)


bp = Blueprint('images', __name__)
bp.add_url_rule('', view_func=ImagesView.as_view('upload_image'))
bp.add_url_rule('/<image_name>', view_func=ImageView.as_view('download_image'))