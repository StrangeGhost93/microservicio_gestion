from flask import Blueprint, jsonify, request

from app.schemas import AsignacionSchema, CohorteSchema
from app.services import CohorteService
from app.validators import validate_with

cohorte_bp = Blueprint("cohortes", __name__)
cohorte_schema = CohorteSchema()


@cohorte_bp.get("/cohortes")
def listar_cohortes():
    programa_id = request.args.get("programa", type=int)
    estado = request.args.get("estado")

    cohortes = CohorteService.listar(programa_id, estado)
    return jsonify(cohorte_schema.dump(cohortes, many=True)), 200


@cohorte_bp.post("/cohortes")
@validate_with(CohorteSchema)
def crear_cohorte(payload):
    creado = CohorteService.crear(payload)
    return jsonify(cohorte_schema.dump(creado)), 201


@cohorte_bp.get("/cohortes/<int:cohorte_id>")
def obtener_cohorte(cohorte_id: int):
    cohorte = CohorteService.obtener(cohorte_id)
    if not cohorte:
        return jsonify({"message": "Cohorte no encontrada"}), 404
    return jsonify(cohorte_schema.dump(cohorte)), 200


@cohorte_bp.put("/cohortes/<int:cohorte_id>")
@validate_with(CohorteSchema)
def actualizar_cohorte(payload, cohorte_id: int):
    actualizado = CohorteService.actualizar(cohorte_id, payload)
    if not actualizado:
        return jsonify({"message": "Cohorte no encontrada"}), 404
    return jsonify(cohorte_schema.dump(actualizado)), 200


@cohorte_bp.delete("/cohortes/<int:cohorte_id>")
def eliminar_cohorte(cohorte_id: int):
    eliminado = CohorteService.eliminar(cohorte_id)
    if not eliminado:
        return jsonify({"message": "Cohorte no encontrada"}), 404
    return jsonify({"message": "Cohorte eliminada"}), 200


@cohorte_bp.post("/cohortes/<int:cohorte_id>/docentes")
@validate_with(AsignacionSchema)
def asignar_docente(payload, cohorte_id: int):
    docente_id = payload.get("docente_id")
    modulo_id = payload.get("modulo_id")
    asignacion = CohorteService.asignar_docente(
        cohorte_id,
        docente_id,
        modulo_id,
        payload.get("horas_semanales", 4),
    )
    if not asignacion:
        return jsonify({"message": "No se pudo generar la asignación"}), 404
    return jsonify({
        "cohorte_id": asignacion.cohorte_id,
        "docente_id": asignacion.docente_id,
        "modulo_id": asignacion.modulo_id,
        "horas_semanales": asignacion.horas_semanales,
    }), 201
