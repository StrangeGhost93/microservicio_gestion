from marshmallow import Schema, fields, validate


class AsignacionSchema(Schema):
    docente_id = fields.Integer(required=True)
    modulo_id = fields.Integer(required=True)
    horas_semanales = fields.Integer(load_default=4, validate=validate.Range(min=1, max=20))
