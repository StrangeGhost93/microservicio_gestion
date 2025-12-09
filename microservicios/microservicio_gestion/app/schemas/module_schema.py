from marshmallow import Schema, fields, validate


class ModuloSchema(Schema):
    id = fields.Integer(dump_only=True)
    titulo = fields.String(required=True, validate=validate.Length(min=3, max=120))
    duracion_semanas = fields.Integer(required=True, validate=validate.Range(min=1, max=52))
    creditos = fields.Integer(load_default=0, validate=validate.Range(min=0, max=60))
    resultados = fields.String(load_default=None)
    programa_id = fields.Integer(dump_only=True)

