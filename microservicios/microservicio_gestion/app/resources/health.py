"""Healthcheck blueprint used by infra and other microservices."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/status")
def status():
    """Return a simple JSON payload to confirm the service is alive."""
    return jsonify({"service": "gestion", "status": "ok"}), 200
