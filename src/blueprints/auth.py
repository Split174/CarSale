from flask import (
    Blueprint,
    request,
    session,
)
from werkzeug.security import check_password_hash
from database import db
from services.user import UserService

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    """
    Вход в акк
    :return:
    """
    request_json = request.json
    email = request_json.get('email')
    password = request_json.get('password')

    if not email or not password:
        return '', 401

    user_service = UserService(db.connection)
    user = user_service.get_user_by_email(email)
    if user is None:
        return 'Пользователя с таким email не существует', 401

    if not check_password_hash(user.password, password):
        return 'Не верный пароль', 401

    session['user_id'] = user.id
    return '', 200


@bp.route('/logout', methods=['POST'])
def logout():
    """
    Выход
    """
    session.pop('user_id', None)
    return '', 200