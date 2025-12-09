from flask import Blueprint, jsonify, request

from app.schemas import ModuloSchema
from app.services import ModuloService
from app.validators import validate_with

modulo_bp = Blueprint("modulos", __name__)
modulo_schema = ModuloSchema()


@modulo_bp.get("/modulos")
def listar_modulos():
    programa_id = request.args.get("programa", type=int)
    modulos = ModuloService.listar(programa_id)
    return jsonify(modulo_schema.dump(modulos, many=True)), 200


@modulo_bp.get("/programas/<int:programa_id>/modulos")
def listar_modulos_por_programa(programa_id: int):
    modulos = ModuloService.listar(programa_id)
    return jsonify(modulo_schema.dump(modulos, many=True)), 200


@modulo_bp.post("/programas/<int:programa_id>/modulos")
@validate_with(ModuloSchema)
def crear_modulo(payload, programa_id: int):
    payload["programa_id"] = programa_id
    creado = ModuloService.crear(payload)
    return jsonify(modulo_schema.dump(creado)), 201


@modulo_bp.delete("/modulos/<int:modulo_id>")
def eliminar_modulo(modulo_id: int):
    eliminado = ModuloService.eliminar(modulo_id)
    if not eliminado:
        return jsonify({"message": "Módulo no encontrado"}), 404
    return jsonify({"message": "Módulo eliminado"}), 200
