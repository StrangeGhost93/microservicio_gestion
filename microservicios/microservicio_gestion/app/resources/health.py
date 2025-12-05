"""Blueprint de healthcheck consumido por la infraestructura y otros servicios."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/status")
def status():
    """Responder un JSON sencillo para confirmar que el servicio está sano."""
    return jsonify({"service": "gestion", "status": "ok"}), 200
