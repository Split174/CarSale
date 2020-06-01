from flask import (
    Blueprint,
    jsonify,
    request,
    session,
    current_app
)
from flask.views import MethodView
from database import db
from werkzeug.utils import secure_filename
import os


bp = Blueprint('images', __name__)


class ImagesView(MethodView):
    def post(self):
        if session.get('user_id') is None:
            return '', 401
        #print(request.data)
        file = request.data
        #filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['IMG_FOLDER'], "filename"))
        return f'/images/filename', 201

    def get(self, name):
        with db.connection as con:
            cur = con.execute("""
                SELECT *
                FROM image
                WHERE image.name = ?""",
                (name,))
            image = cur.fetchone()
            if image is not None:
                return dict(image), 200


bp.add_url_rule('', view_func=ImagesView.as_view('images'))
bp.add_url_rule('/<name>', view_func=ImagesView.as_view('images_get'))