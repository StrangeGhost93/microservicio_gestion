"""Healthcheck del servicio de gestión."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/status")
def status():
    return jsonify({"service": "gestion", "status": "ok"}), 200
