from flask import (
    Blueprint,
    request,
    session,
    jsonify
)
from flask.views import MethodView
from werkzeug.security import check_password_hash
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
        with db.connection as con:
            cur = con.execute("""
            SELECT *
            FROM ad
            """)
            return jsonify([dict(row) for row in cur.fetchall()]), 200

    def post(self):
        """Запостить объявление"""
        user_id = session.get('user_id')
        if user_id is None:
            return '', 401
        request_json = request.json
        title = request_json.get('title')
        make = request_json.get('car').get('make')
        model = request_json.get('car').get('model')
        mileage = request_json.get('car').get('mileage')
        num_owners = request_json.get('car').get('num_owners')
        reg_number = request_json.get('car').get('reg_number')
        with db.connection as con:
            cur = con.execute("""
                        INSERT INTO car (make, model, mileage, num_owners, reg_number)
                        VALUES (?, ?, ?, ?, ?)""",
                        (make, model, mileage, num_owners, reg_number),
                        )
            con.commit()
            car_id = cur.lastrowid
            con.execute("""
                INSERT INTO ad (title, seller_id, car_id, date)
                VALUES (?, ?, ?, ?)""",
                (title, user_id, car_id, time.time()),
            )
            con.commit()
            ad_id = cur.lastrowid
            ad = {

            }

            cur = con.execute("""
            SELECT *
            FROM ad LEFT JOIN car ON ad.car_id = car.id
            WHERE ad.seller_id = ?
            """,
            (user_id,))
            return dict(cur.fetchone()), 201

class AdView(MethodView):
    """
    Получить объявления по id
    """
    def get(self, user_id):
        with db.connection as con:
            cur = con.execute("""
                    SELECT *
                    FROM ad LEFT JOIN car ON ad.car_id = car.id
                    WHERE ad.id = ?
                    """,
                    (user_id,))
        return dict(cur.fetchone()), 200

class DeleteAdsView(MethodView):
    """
    Удалить объявление
    """
    def delete(self, ad_id):
        with db.connection as con:
            print('qq')
            user_id = session.get('user_id')
            if user_id is None:
                return '', 401
            cur = con.execute("""
                    SELECT *
                    FROM ad
                    WHERE ad.id = ?
                    """,
                    (ad_id,))
            ad = cur.fetchone()
            if ad is not None:
                ad = dict(ad)
            if ad['seller_id'] != user_id:
                return '', 401
            con.execute("""
            DELETE FROM ad WHERE id = ?
            """,
            (ad_id,))
            con.commit()
            return '', 200


bp.add_url_rule('', view_func=AdsView.as_view('ads'))
bp.add_url_rule('/<int:user_id>', view_func=AdView.as_view('ad_get'))
bp.add_url_rule('/<int:ad_id>', view_func=DeleteAdsView.as_view('ad_del'))

