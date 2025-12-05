from flask import Blueprint, jsonify, request

from app.extensions import hashids
from app.schemas import AsignacionSchema, CohorteSchema
from app.services import CohorteService
from app.validators import validate_with

cohorte_bp = Blueprint("cohortes", __name__)
cohorte_schema = CohorteSchema()
asignacion_schema = AsignacionSchema()


def _decode_hashid(value: str | None) -> int | None:
    if not value:
        return None
    decoded = hashids.decode(value)
    return decoded[0] if decoded else None


@cohorte_bp.get("/cohortes")
def listar_cohortes():
    programa_hashid = request.args.get("programa")
    estado = request.args.get("estado")
    programa_id = _decode_hashid(programa_hashid)

    cohortes = CohorteService.listar(programa_id, estado)
    return jsonify(cohorte_schema.dump(cohortes, many=True)), 200


@cohorte_bp.post("/cohortes")
@validate_with(CohorteSchema)
def crear_cohorte(payload):
    creado = CohorteService.crear(payload)
    return jsonify(cohorte_schema.dump(creado)), 201


@cohorte_bp.get("/cohortes/<hashid:cohorte_id>")
def obtener_cohorte(cohorte_id: int):
    cohorte = CohorteService.obtener(cohorte_id)
    if not cohorte:
        return jsonify({"message": "Cohorte no encontrada"}), 404
    return jsonify(cohorte_schema.dump(cohorte)), 200


@cohorte_bp.put("/cohortes/<hashid:cohorte_id>")
@validate_with(CohorteSchema)
def actualizar_cohorte(payload, cohorte_id: int):
    actualizado = CohorteService.actualizar(cohorte_id, payload)
    if not actualizado:
        return jsonify({"message": "Cohorte no encontrada"}), 404
    return jsonify(cohorte_schema.dump(actualizado)), 200


@cohorte_bp.delete("/cohortes/<hashid:cohorte_id>")
def eliminar_cohorte(cohorte_id: int):
    eliminado = CohorteService.eliminar(cohorte_id)
    if not eliminado:
        return jsonify({"message": "Cohorte no encontrada"}), 404
    return jsonify({"message": "Cohorte eliminada"}), 200


@cohorte_bp.post("/cohortes/<hashid:cohorte_id>/docentes")
@validate_with(AsignacionSchema)
def asignar_docente(payload, cohorte_id: int):
    docente_id = _decode_hashid(payload.get("docente_hashid"))
    modulo_id = _decode_hashid(payload.get("modulo_hashid"))
    if not docente_id or not modulo_id:
        return jsonify({"message": "Identificadores inválidos"}), 400
    asignacion = CohorteService.asignar_docente(
        cohorte_id,
        docente_id,
        modulo_id,
        payload.get("horas_semanales", 4),
    )
    if not asignacion:
        return jsonify({"message": "No se pudo generar la asignación"}), 404
    return jsonify({
        "cohorte": hashids.encode(asignacion.cohorte_id),
        "docente": hashids.encode(asignacion.docente_id),
        "modulo": hashids.encode(asignacion.modulo_id),
        "horas_semanales": asignacion.horas_semanales,
    }), 201
