import unittest
from flask import current_app
from app import create_app
from app.models import Facultad
from app import db
import os

from app.services.facultad_service import FacultadService

class FacultadTestCase(unittest.TestCase):
    def _nuevaFacultad(self):
        facultad = Facultad()
        facultad.nombre = "Facultad de Ciencias Exactas"
        facultad.abreviatura = "FCE"
        facultad.directorio = "Ciencias Exactas"
        facultad.sigla = "FCE"
        facultad.codigo_postal = "12345"
        facultad.ciudad = "La Plata"
        facultad.domicilio = "Calle 123"
        facultad.telefono = "123456789"
        facultad.contacto = "Juan Perez"
        facultad.email = "abc@gmail.com"
        return facultad

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_facultad_creation(self):
        facultad = self._nuevaFacultad()
        self.assertIsNotNone(facultad)
        self.assertEqual(facultad.nombre, "Facultad de Ciencias Exactas")
        self.assertEqual(facultad.abreviatura, "FCE")

    def _nuevaFacultad(self):
        facultad = Facultad()
        facultad.nombre = "Facultad de Ciencias Exactas"
        facultad.abreviatura = "FCE"
        facultad.directorio = "Ciencias Exactas"
        facultad.sigla = "FCE"
        facultad.codigo_postal = "12345"
        facultad.ciudad = "La Plata"
        facultad.domicilio = "Calle 123"
        facultad.telefono = "123456789"
        facultad.contacto = "Juan Perez"
        facultad.email = "abc@gmail.com"
        return facultad
    def test_facultad_busqueda(self):
        facultad = self._nuevaFacultad()
        FacultadService.crear_facultad(facultad)
        FacultadService.buscar_por_id(facultad.id)
        self.assertEqual(facultad.nombre, "Facultad de Ciencias Exactas")
        self.assertEqual(facultad.abreviatura, "FCE")