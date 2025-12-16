from datetime import date
from app.models.tipo_documento import TipoDocumento

class Alumno:
    def __init__(self, apellido: str, nombre: str, nroDocumento: str, tipoDocumento: TipoDocumento,
                 fechaNacimiento: str, sexo: str, nroLegajo: int, fechaIngreso: date):
        self.apellido = apellido
        self.nombre = nombre
        self.nroDocumento = nroDocumento
        self.tipoDocumento = tipoDocumento
        self.fechaNacimiento = fechaNacimiento
        self.sexo = sexo
        self.nroLegajo = nroLegajo
        self.fechaIngreso = fechaIngreso