import os
from flask import Flask

from .config import config_by_name
from .extensions import db, migrate, ma, hashids, cache, limiter
from .resources import register_blueprints


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    env_name = config_name or os.getenv("FLASK_ENV", "development")
    config_class = config_by_name.get(env_name, config_by_name["development"])
    app.config.from_object(config_class)
    config_class.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    hashids.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    register_blueprints(app)

    from . import models  # noqa: WPS433  (circular import guard)

    @app.shell_context_processor
    def ctx():
        exported = {name: getattr(models, name) for name in dir(models) if name[0].isupper()}
        exported["db"] = db
        return exported

    return app


# Alias compatible con gunicorn cuando se apunta a "app:app"
app = create_app()
