from flask import Flask

from .resources import register_blueprints


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    register_blueprints(app)
    return app


app = create_app()
