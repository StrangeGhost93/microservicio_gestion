import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import config
from app.resources import register_blueprints

# Instancias globales de extensiones
db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    """
    Factory de la aplicación con DB, migraciones y blueprints de API.
    """
    app_context = os.getenv("FLASK_CONTEXT")
    app = Flask(__name__)
    f = config.factory(app_context if app_context else "development")
    app.config.from_object(f)

    # Conecta extensiones
    db.init_app(app)

    # Importa modelos para que Flask-Migrate detecte metadatos
    with app.app_context():
        from app.models.especialidad import Especialidad  # noqa: F401

    migrate.init_app(app, db)

    # Registrar blueprints (API + certificados)
    register_blueprints(app)

    # Atajo para shell
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
