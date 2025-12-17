import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app, db
from app.repositories.especialidad_repository import EspecialidadRepository


@pytest.fixture
def app():
    os.environ["FLASK_CONTEXT"] = "testing"
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    db.create_all()

    seed_rows = [
        {"especialidad": "Ingenieria en Sistemas", "facultad": "Facultad de Ingenieria", "universidad": "UNL"},
        {"especialidad": "Administracion de Empresas", "facultad": "Ciencias Economicas", "universidad": "UBA"},
    ]
    EspecialidadRepository().bulk_seed(seed_rows)

    yield app

    db.session.remove()
    db.drop_all()
    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()

