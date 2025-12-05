"""Endpoints de integración con otros microservicios del ecosistema."""

from flask import Blueprint, jsonify

from app.extensions import limiter
from app.integrations.documentacion_client import DocumentacionClient

integracion_bp = Blueprint("integraciones", __name__)


@integracion_bp.get("/integraciones/documentacion/status")
@limiter.limit("5/minute")
def estado_documentacion():
    """Consultar el estado del microservicio de documentación con circuit breaker."""
    payload, status = DocumentacionClient.estado_servicio()
    return jsonify(payload), status
