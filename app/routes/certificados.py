from flask import Blueprint, Response
from app.models.alumno import Alumno
from app.models.tipo_documento import TipoDocumento
from app.services.certificados import generar_alumno_certificado
from datetime import date

certificados_bp = Blueprint('certificados', __name__)

@certificados_bp.route('/certificado/<int:legajo>')
def certificado_pdf(legajo):
    alumno = Alumno(
    apellido="Gómez",
    nombre="María",
    nroDocumento=str(legajo),
    tipoDocumento=TipoDocumento.DNI,
    fechaNacimiento="2002-04-20",
    sexo="F",
    nroLegajo=legajo,
    fechaIngreso=date(2023, 3, 1)
)

    pdf_bytes = generar_alumno_certificado(alumno)

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"inline; filename=certificado_{alumno.nroDocumento}.pdf"}
    )
