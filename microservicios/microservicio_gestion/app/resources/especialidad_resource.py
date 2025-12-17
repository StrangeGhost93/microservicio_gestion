"""Endpoints CRUD mínimos para especialidades respaldadas en DB."""

from flask import Blueprint, jsonify

from app.services.especialidad_service import EspecialidadService

especialidad_bp = Blueprint("especialidades", __name__)
_service = EspecialidadService()


def _to_dict(especialidad):
    return {
        "id": especialidad.id,
        "especialidad": especialidad.especialidad,
        "facultad": especialidad.facultad,
        "universidad": especialidad.universidad,
    }


@especialidad_bp.get("/especialidades")
def listar_especialidades():
    especialidades = _service.listar()
    return jsonify([_to_dict(e) for e in especialidades]), 200


@especialidad_bp.get("/especialidades/<int:especialidad_id>")
def obtener_especialidad(especialidad_id: int):
    especialidad = _service.obtener(especialidad_id)
    if not especialidad:
        return jsonify({"message": "Especialidad no encontrada"}), 404
    return jsonify(_to_dict(especialidad)), 200
