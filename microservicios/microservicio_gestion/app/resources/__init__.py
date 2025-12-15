from flask import Flask

from .especialidad_resource import especialidad_bp
from .health import health_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(especialidad_bp, url_prefix="/api/v1")
