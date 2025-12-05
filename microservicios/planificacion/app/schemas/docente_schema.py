from marshmallow import Schema, fields, validate


class DocenteSchema(Schema):
    hashid = fields.String(attribute="hashid", dump_only=True)
    nombre = fields.String(required=True, validate=validate.Length(min=2, max=80))
    apellido = fields.String(required=True, validate=validate.Length(min=2, max=80))
    email = fields.Email(required=True)
    especialidad = fields.String(load_default=None)
    horas_disponibles = fields.Integer(load_default=10, validate=validate.Range(min=2, max=40))

