from flask import (
    Blueprint,
    request,
    session,
    jsonify
)
from flask.views import MethodView
from services.ads import AdsService
from services.user import UserService
from services.car import CarService
from database import db
import sqlite3
import time


bp = Blueprint('ads', __name__)


class AdsView(MethodView):
    def get(self):
        """
        Вывести все объявления
        :return: Объявления
        """
        ads_service = AdsService(db.connection)
        ads = ads_service.get_all_ads()
        return jsonify(ads), 200

    def post(self):
        """Запостить объявление"""
        user_id = session.get('user_id')
        if user_id is None:
            return '', 401
        user_service = UserService(db.connection)
        if not user_service.is_user_a_seller(user_id):
            return 'Пользователь не является продавцом', 403
        request_json = request.json
        ad_title = request_json.get('title')
        car = {
            'make': request_json.get('car').get('make'),
            'model': request_json.get('car').get('model'),
            'mileage': request_json.get('car').get('mileage'),
            'num_owners': request_json.get('car').get('num_owners'),
            'reg_number': request_json.get('car').get('reg_number'),
        }
        car_service = CarService(db.connection)
        new_car = car_service.add_car(car)
        ad_service = AdsService(db.connection)
        new_ad = ad_service.add_ad(ad_title, session.get('user_id'), new_car['id'])
        return jsonify(ad_service.get_ad_by_id(new_ad['id'])), 200


class AdView(MethodView):
    def get(self, ad_id):
        """
        Получить объявление по id
        """
        ad_service = AdsService(db.connection)
        return jsonify(ad_service.get_ad_by_id(ad_id)), 200

    def delete(self, ad_id):
        """
            Удалить объявление
        """
        user_id = session.get('user_id')
        if user_id is None:
            return '', 401
        ad_service = AdsService(db.connection)
        if not ad_service.is_ad_belong_user(user_id, ad_id):
            return '', 403
        ad_service.delete_ad(ad_id)
        return '', 200


bp.add_url_rule('', view_func=AdsView.as_view('ads'))
bp.add_url_rule('/<int:ad_id>', view_func=AdView.as_view('ad_del_add'))

