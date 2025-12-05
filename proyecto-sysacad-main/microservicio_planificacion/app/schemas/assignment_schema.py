from marshmallow import Schema, fields, validate


class AsignacionSchema(Schema):
    docente_hashid = fields.String(required=True)
    modulo_hashid = fields.String(required=True)
    horas_semanales = fields.Integer(load_default=4, validate=validate.Range(min=1, max=20))
