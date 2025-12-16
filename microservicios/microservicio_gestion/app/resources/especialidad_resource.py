"""Endpoints CRUD mínimos para especialidades mock."""

from flask import Blueprint, jsonify

from app.services.especialidad_service import EspecialidadService

especialidad_bp = Blueprint("especialidades", __name__)


@especialidad_bp.get("/especialidades")
def listar_especialidades():
    especialidades = EspecialidadService.listar()
    return jsonify(especialidades), 200


@especialidad_bp.get("/especialidades/<int:especialidad_id>")
def obtener_especialidad(especialidad_id: int):
    especialidad = EspecialidadService.obtener(especialidad_id)
    if not especialidad:
        return jsonify({"message": "Especialidad no encontrada"}), 404
    return jsonify(especialidad), 200
