from marshmallow import Schema, fields, validate


class ProgramaSchema(Schema):
    hashid = fields.String(attribute="hashid", dump_only=True)
    nombre = fields.String(required=True, validate=validate.Length(min=3, max=120))
    version = fields.String(required=True, validate=validate.Length(min=1, max=40))
    modalidad = fields.String(required=True, validate=validate.Length(min=2, max=40))
    descripcion = fields.String(load_default=None)
    duracion_meses = fields.Integer(required=True, validate=validate.Range(min=3, max=72))
    creditos_totales = fields.Integer(load_default=0, validate=validate.Range(min=0))
    vigente = fields.Boolean(load_default=True)

