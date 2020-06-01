from flask import (
    Blueprint,
    request,
    session,
    jsonify
)
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from database import db
import sqlite3

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
        is_seller = True if request_json.get('is_seller').lower() == 'true' else False
        if is_seller:
            seller = {
                'phone': request_json.get('phone'),
                'zip_code': request_json.get('zip_code'),
                'city_id': request_json.get('city_id'),
                'street': request_json.get('street'),
                'home': request_json.get('home')
            }

        password_hash = generate_password_hash(account["password"])
        account_id = -1
        with db.connection as con:
            try:
                cursor = con.execute(
                    'INSERT INTO account (email, password, first_name, last_name)'
                    'VALUES (?, ?, ?, ?)',
                    (account["email"], password_hash, account["first_name"], account["last_name"]),
                )
                con.commit()
                account_id = cursor.lastrowid
            except sqlite3.IntegrityError:
                return '', 409

        print(account_id)
        if is_seller:
            seller['account_id'] = account_id
            with db.connection as con:
                try:
                    con.execute(
                        'INSERT INTO seller (phone, zip_code, street, home, account_id) '
                        'VALUES (?, ?, ?, ?, ?)',
                        (seller['phone'], seller['zip_code'], seller['street'], seller['home'], seller['account_id']),
                    )
                    con.commit()
                    con.execute(
                        'INSERT INTO zipcode (zip_code, city_id) '
                        'VALUES (?, ?)',
                        (seller['zip_code'], seller['city_id']),
                    )
                    con.commit()
                except sqlite3.IntegrityError:
                    return '', 409

        account['id'] = account_id
        account['is_seller'] = is_seller
        account.pop('password')
        if is_seller:
            account.update(seller)
        return account


class UserView(MethodView):
    def get(self, user_id):
        """
        Получить пользователя/продавца
        :param user_id: id пользователя
        :return:
        """
        if session.get('user_id') is None:
            return
        with db.connection as con:
            cur = con.execute(
                """SELECT id, email, first_name, last_name
                FROM account
                WHERE id = ?""",
                (user_id,)
            )
            user = dict(cur.fetchone())
            con.commit()
            cur = con.execute(
                """SELECT phone, zip_code, street, home
                FROM seller
                WHERE account_id = ?""",
                (user['id'],)
            )
            seller = cur.fetchone()
            con.commit()
            if seller is not None:
                seller = dict(seller)
                user['is_seller'] = True
                user['phone'] = seller['phone']
                user['zip_code'] = seller['zip_code']
                user['street'] = seller['street']
                user['home'] = seller['home']

                cur = con.execute(
                    """SELECT city_id
                    FROM zipcode
                    WHERE zip_code = ?""",
                    (user['zip_code'],)
                )
                user['city_id'] = dict(cur.fetchone())['city_id']
                con.commit()

        return jsonify(user)

class UserAdsView(MethodView):
    """Получить объявление по Seller_id"""
    def get(self, user_id):
        with db.connection as con:
            cur = con.execute("""
            SELECT *
            FROM ad
            WHERE seller_id = ?
            """,
            (user_id,))
            return jsonify([dict(row) for row in cur.fetchall()]), 200


bp.add_url_rule('', view_func=UsersView.as_view('users'))
bp.add_url_rule('/<int:user_id>', view_func=UserView.as_view('user'))
bp.add_url_rule('/<int:user_id>/ads', view_func=UserAdsView.as_view('user_ads'))



