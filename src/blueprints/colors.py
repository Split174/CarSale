from flask import (
    Blueprint,
    jsonify,
    request,
    session
)
from flask.views import MethodView
from services.colors import ColorService
from services.user import UserService
from database import db
from sqlalchemy.exc import IntegrityError
import sqlite3

class ColorsView(MethodView):
    def get(self):
        """
        Получить все цвета
        :return:
        """
        if session.get('user_id') is None:
            return '', 401
        user_service = UserService(db.connection)
        if not user_service.is_user_a_seller(session.get('user_id')):
            return 'получать цвета могут только продавцы', 405
        color_service = ColorService(db.connection)
        return jsonify(color_service.get_colors()), 200

    def post(self):
        """
        Добавить цвет
        """
        if session.get('user_id') is None:
            return '', 401
        user_service = UserService(db.connection)
        if not user_service.is_user_a_seller(session.get('user_id')):
            return 'добавлять цвет могут только продавцы', 403
        request_json = request.json
        name = request_json.get('name')
        hex = request_json.get('hex')
        color_service = ColorService(db.connection)
        color = color_service.get_color_by_name(name)
        if color is not None:
            return jsonify(color.as_dict()), 201
        try:
            return jsonify(color_service.add_color(name, hex)), 201
        except IntegrityError:
            return '', 404


bp = Blueprint('colors', __name__)
bp.add_url_rule('', view_func=ColorsView.as_view('colors'))

