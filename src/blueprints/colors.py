from flask import (
    Blueprint,
    jsonify,
    request,
    session
)
from flask.views import MethodView
from database import db
bp = Blueprint('colors', __name__)


class ColorsView(MethodView):
    def get(self):
        """
        Получить все цвета
        :return:
        """
        with db.connection as con:
            cur = con.execute("""
                        SELECT *
                        FROM color
                        """)
            return jsonify([dict(row) for row in cur.fetchall()]), 200

    def post(self):
        """
        Добавить цвет
        :return:
        """
        if session.get('user_id') is None:
            return '', 401
        request_json = request.json
        name = request_json.get('name')
        hex = request_json.get('hex')
        with db.connection as con:
            cur = con.execute("""
                    SELECT *
                    FROM color
                    WHERE name = ?""",
                    (name,))
            color = cur.fetchone()
            if color is not None:
                return dict(color), 200
            cur = con.execute("""
                    INSERT INTO color (hex, name)
                    VALUES (?, ?)""",
                    (hex, name))
            con.commit()
            cur = con.execute("""
                    SELECT *
                    FROM color
                    WHERE name = ?
                    """,
                    (name,))
            return dict(cur.fetchone()), 302


bp.add_url_rule('', view_func=ColorsView.as_view('colors'))