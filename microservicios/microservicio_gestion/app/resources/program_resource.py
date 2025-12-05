"""Blueprint que expone el CRUD de programas con validaciones coherentes."""

from flask import Blueprint, jsonify, request

from app.schemas import ProgramaSchema
from app.services import ProgramaService
from app.validators import validate_with

programa_bp = Blueprint("programas", __name__)
programa_schema = ProgramaSchema()


def _parse_bool(value: str | None) -> bool | None:
    """Convertir strings comunes en booleanos considerando variante locales."""
    if value is None:
        return None
    return value.lower() in {"true", "1", "si", "yes"}


@programa_bp.get("/programas")
def listar_programas():
    """Listar los programas en función del filtro `vigente` opcional."""
    vigente = _parse_bool(request.args.get("vigente"))
    programas = ProgramaService.listar(vigente)
    return jsonify(programa_schema.dump(programas, many=True)), 200


@programa_bp.post("/programas")
@validate_with(ProgramaSchema)
def crear_programa(programa):
    """Crear un programa usando el payload validado por Marshmallow."""
    creado = ProgramaService.crear(programa)
    return jsonify(programa_schema.dump(creado)), 201


@programa_bp.get("/programas/<hashid:programa_id>")
def obtener_programa(programa_id: int):
    """Recuperar un programa puntual utilizando hashid resuelto a ID interno."""
    programa = ProgramaService.obtener(programa_id)
    if not programa:
        return jsonify({"message": "Programa no encontrado"}), 404
    return jsonify(programa_schema.dump(programa)), 200


@programa_bp.put("/programas/<hashid:programa_id>")
@validate_with(ProgramaSchema)
def actualizar_programa(payload, programa_id: int):
    """Actualizar el programa indicado y retornar su representación serializada."""
    actualizado = ProgramaService.actualizar(programa_id, payload)
    if not actualizado:
        return jsonify({"message": "Programa no encontrado"}), 404
    return jsonify(programa_schema.dump(actualizado)), 200


@programa_bp.delete("/programas/<hashid:programa_id>")
def eliminar_programa(programa_id: int):
    """Eliminar un programa existente retornando 404 si no se halló."""
    eliminado = ProgramaService.eliminar(programa_id)
    if not eliminado:
        return jsonify({"message": "Programa no encontrado"}), 404
    return jsonify({"message": "Programa eliminado"}), 200
