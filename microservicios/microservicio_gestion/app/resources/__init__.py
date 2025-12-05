from flask import Flask

from .cohort_resource import cohorte_bp
from .docente_resource import docente_bp
from .health import health_bp
from .module_resource import modulo_bp
from .program_resource import programa_bp
from .integration_resource import integracion_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(programa_bp, url_prefix="/api/v1")
    app.register_blueprint(modulo_bp, url_prefix="/api/v1")
    app.register_blueprint(cohorte_bp, url_prefix="/api/v1")
    app.register_blueprint(docente_bp, url_prefix="/api/v1")
    app.register_blueprint(integracion_bp, url_prefix="/api/v1")
