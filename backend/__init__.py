from flask import Flask

from backend.model import init_db


def init_app():
    app = Flask(__name__)
    init_db()
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")
    return app
