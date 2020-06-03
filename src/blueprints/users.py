from flask import (
    Blueprint,
    request,
    session,
    jsonify
)
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from database import db
from services.user import UserService
from services.cities import CityService
from services.ads import AdsService


bp = Blueprint('users', __name__)


class UsersView(MethodView):
    def post(self):
        """
        Создать пользователя/продавца
        :return:
        """
        request_json = request.json
        account = {
            'email': request_json.get('email'),
            'password': request_json.get('password'),
            'first_name': request_json.get('first_name'),
            'last_name': request_json.get('last_name')
        }
        is_seller = request_json.get('is_seller')
        if is_seller:
            seller = {
                'phone': request_json.get('phone'),
                'zip_code': request_json.get('zip_code'),
                'city_id': request_json.get('city_id'),
                'street': request_json.get('street'),
                'home': request_json.get('home')
            }

        password_hash = generate_password_hash(account["password"])
        user_service = UserService(db.connection)
        new_user = user_service.add_account(account, password_hash)
        print(new_user)
        if is_seller:
            city_service = CityService(db.connection)
            if city_service.get_zipcode(seller['zip_code']) is None:
                city_service.add_zipcode(seller['zip_code'], seller['city_id'])
            new_seller = user_service.add_seller(seller, new_user['id'])
            return {**new_user, **{'is_seller': is_seller}, **new_seller}, 201
        return {**new_user, **{'is_seller': is_seller}}, 201


class UserView(MethodView):
    def get(self, user_id):
        """
        Получить пользователя/продавца
        :param user_id: id пользователя
        :return:
        """
        if session.get('user_id') is None:
            return '', 401
        user_service = UserService(db.connection)
        return jsonify(user_service.get_user(user_id)), 200


class UserAdsView(MethodView):
    """Получить объявление по Seller_id"""

    def get(self, user_id):
        ads_service = AdsService(db.connection)
        return jsonify(ads_service.get_all_users_ads(user_id)), 200


bp.add_url_rule('', view_func=UsersView.as_view('users'))
bp.add_url_rule('/<int:user_id>', view_func=UserView.as_view('user'))
bp.add_url_rule('/<int:user_id>/ads', view_func=UserAdsView.as_view('user_ads'))



