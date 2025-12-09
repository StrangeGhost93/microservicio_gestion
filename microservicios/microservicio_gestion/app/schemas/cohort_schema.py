from marshmallow import Schema, fields, validate


class CohorteSchema(Schema):
    id = fields.Integer(dump_only=True)
    anio = fields.Integer(required=True, validate=validate.Range(min=2000, max=2100))
    campus = fields.String(required=True, validate=validate.Length(min=2, max=80))
    modalidad = fields.String(required=True, validate=validate.Length(min=2, max=40))
    cupo = fields.Integer(required=True, validate=validate.Range(min=5, max=200))
    fecha_inicio = fields.String(required=True)
    fecha_fin = fields.String(load_default=None)
    estado = fields.String(load_default="planificada")
    programa_id = fields.Integer(required=True)

