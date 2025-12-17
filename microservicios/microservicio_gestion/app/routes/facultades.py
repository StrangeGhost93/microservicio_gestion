from flask import Blueprint, request, Response
from app.services.csv_utils import facultades_to_csv
from app.services.facultad_service import FacultadService

facultades_bp = Blueprint("facultades", __name__)


@facultades_bp.route("/facultades/export", methods=["GET"])
def export_facultades():
    fmt = request.args.get("format", "csv").lower()
    if fmt != "csv":
        return ("Unsupported format", 400)

    facultades = FacultadService.buscar_todos()
    csv_bytes = facultades_to_csv(facultades)
    return Response(csv_bytes, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=facultades.csv"})
