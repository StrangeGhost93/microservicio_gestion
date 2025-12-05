from flask import Blueprint, jsonify, request

from app.schemas import ProgramaSchema
from app.services import ProgramaService
from app.validators import validate_with

programa_bp = Blueprint("programas", __name__)
programa_schema = ProgramaSchema()


def _parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    return value.lower() in {"true", "1", "si", "yes"}


@programa_bp.get("/programas")
def listar_programas():
    vigente = _parse_bool(request.args.get("vigente"))
    programas = ProgramaService.listar(vigente)
    return jsonify(programa_schema.dump(programas, many=True)), 200


@programa_bp.post("/programas")
@validate_with(ProgramaSchema)
def crear_programa(programa):
    creado = ProgramaService.crear(programa)
    return jsonify(programa_schema.dump(creado)), 201


@programa_bp.get("/programas/<hashid:programa_id>")
def obtener_programa(programa_id: int):
    programa = ProgramaService.obtener(programa_id)
    if not programa:
        return jsonify({"message": "Programa no encontrado"}), 404
    return jsonify(programa_schema.dump(programa)), 200


@programa_bp.put("/programas/<hashid:programa_id>")
@validate_with(ProgramaSchema)
def actualizar_programa(payload, programa_id: int):
    actualizado = ProgramaService.actualizar(programa_id, payload)
    if not actualizado:
        return jsonify({"message": "Programa no encontrado"}), 404
    return jsonify(programa_schema.dump(actualizado)), 200


@programa_bp.delete("/programas/<hashid:programa_id>")
def eliminar_programa(programa_id: int):
    eliminado = ProgramaService.eliminar(programa_id)
    if not eliminado:
        return jsonify({"message": "Programa no encontrado"}), 404
    return jsonify({"message": "Programa eliminado"}), 200
