from functools import wraps

from flask import jsonify, request
from marshmallow import ValidationError


def validate_with(schema_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = schema_class().load(request.get_json() or {})
            except ValidationError as error:
                return jsonify({"errors": error.messages}), 400
            return func(data, *args, **kwargs)

        return wrapper

    return decorator
