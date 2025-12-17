from flask import Flask

 # registro de blueprints 
def register_blueprints(app: Flask) -> None:
	# Importar dentro de la función para evitar ciclos de inicialización
	from app.resources.especialidad_resource import especialidad_bp
	from app.resources.health import health_bp
	from app.routes.certificados import certificados_bp
	from app.routes.facultades import facultades_bp

	app.register_blueprint(health_bp, url_prefix="/api/v1")
	app.register_blueprint(especialidad_bp, url_prefix="/api/v1")
	app.register_blueprint(facultades_bp, url_prefix="/api/v1")
	app.register_blueprint(certificados_bp)
