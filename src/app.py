from flask import Flask
from blueprints.auth import bp as bp_auth
from blueprints.users import bp as bp_users
from blueprints.ads import bp as bp_ads
from blueprints.cities import bp as bp_cities
from blueprints.colors import bp as bp_colors
from blueprints.images import bp as bp_images
from database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_users, url_prefix='/users')
    app.register_blueprint(bp_ads, url_prefix='/ads')
    app.register_blueprint(bp_cities, url_prefix='/cities')
    app.register_blueprint(bp_colors, url_prefix='/colors')
    #app.register_blueprint(bp_images, url_prefix='/images')
    db.init_app(app)
    return app
