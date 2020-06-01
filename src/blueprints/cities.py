from flask import (
    Blueprint,
    jsonify,
    request
)
from flask.views import MethodView
from database import db
import sqlite3

bp = Blueprint('cities', __name__)


class CitiesView(MethodView):
    def post(self):
        """
        Добавить город, если он не существует
        :return:
        """
        request_json = request.json
        name = request_json.get('name')
        with db.connection as con:
            try:
                cur = con.execute("""
                    SELECT *
                    FROM city
                    WHERE city.name = ?""",
                (name,))
                city = cur.fetchone()
                if city is not None:
                    return dict(city), 200

                cur = con.execute("""
                    INSERT INTO city (name)
                    VALUES (?)""",
                    (name,))
                con.commit()
                cur = con.execute("""
                    SELECT *
                    FROM city
                    WHERE name = ?
                    """,
                    (name,))
                return dict(cur.fetchone()), 302
            except sqlite3.IntegrityError:
                return '', 409


bp.add_url_rule('', view_func=CitiesView.as_view('cities'))

