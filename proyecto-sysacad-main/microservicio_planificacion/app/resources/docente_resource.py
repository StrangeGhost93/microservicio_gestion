from flask import Blueprint, jsonify, request

from app.schemas import DocenteSchema
from app.services import DocenteService
from app.validators import validate_with


docente_bp = Blueprint("docentes", __name__)
docente_schema = DocenteSchema()


@docente_bp.get("/docentes")
def listar_docentes():
    especialidad = request.args.get("especialidad")
    docentes = DocenteService.listar(especialidad)
    return jsonify(docente_schema.dump(docentes, many=True)), 200


@docente_bp.post("/docentes")
@validate_with(DocenteSchema)
def crear_docente(payload):
    creado = DocenteService.crear(payload)
    return jsonify(docente_schema.dump(creado)), 201


@docente_bp.get("/docentes/<hashid:docente_id>")
def obtener_docente(docente_id: int):
    docente = DocenteService.obtener(docente_id)
    if not docente:
        return jsonify({"message": "Docente no encontrado"}), 404
    return jsonify(docente_schema.dump(docente)), 200


@docente_bp.put("/docentes/<hashid:docente_id>")
@validate_with(DocenteSchema)
def actualizar_docente(payload, docente_id: int):
    actualizado = DocenteService.actualizar(docente_id, payload)
    if not actualizado:
        return jsonify({"message": "Docente no encontrado"}), 404
    return jsonify(docente_schema.dump(actualizado)), 200


@docente_bp.delete("/docentes/<hashid:docente_id>")
def eliminar_docente(docente_id: int):
    eliminado = DocenteService.eliminar(docente_id)
    if not eliminado:
        return jsonify({"message": "Docente no encontrado"}), 404
    return jsonify({"message": "Docente eliminado"}), 200
