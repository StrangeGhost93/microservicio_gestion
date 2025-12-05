import logging
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from flask_migrate import Migrate

# Creás la instancia global de la base de datos (se va a vincular con app después).
db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    """
    Using an Application Factory
    Ref: Book Flask Web Development Page 78
    """
    app_context = os.getenv('FLASK_CONTEXT')
    #https://flask.palletsprojects.com/en/stable/api/#flask.Flask
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    
    
    # Conecta la instancia de SQLAlchemy con tu app Flask.
    db.init_app(app)
    migrate.init_app(app, db)



    # Esto es un "atajo" para que, si entrás a la shell (flask shell), tengas acceso a app automáticamente.
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    

    # Registrar rutas si usás Blueprint
    from app.routes.certificados import certificados_bp
    app.register_blueprint(certificados_bp)


    return app
