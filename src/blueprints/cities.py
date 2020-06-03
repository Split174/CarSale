from flask import (
    Blueprint,
    jsonify,
    request
)
from flask.views import MethodView
from services.cities import CityService
from database import db

bp = Blueprint('cities', __name__)


class CitiesView(MethodView):
    def post(self):
        """
        Добавить город, если он не существует
        :return:
        """
        request_json = request.json
        name = request_json.get('name')
        city_service = CityService(db.connection)
        city = city_service.get_city_by_name(name)
        if city is not None:
            return jsonify(city.as_dict()), 201 # говорить о том что город добавлен даже если он есть?
        return jsonify(city_service.add_city(name)), 201


class CityView(MethodView):
    def get(self):
        """
        Получить список городов
        :return:
        """
        city_service = CityService(db.connection)
        return jsonify(city_service.get_cities()), 200


bp.add_url_rule('', view_func=CitiesView.as_view('add_city'))
bp.add_url_rule('', view_func=CityView.as_view('get_cities'))

