from app.services.csv_utils import facultades_to_csv
from app.models.facultad import Facultad
from app import db


def test_facultades_to_csv_unit():
    f1 = Facultad()
    f1.id = 1
    f1.nombre = "Facultad A"
    f1.abreviatura = "FA"
    f1.ciudad = "CiudadA"

    f2 = Facultad()
    f2.id = 2
    f2.nombre = "Facultad B"
    f2.abreviatura = "FB"
    f2.ciudad = "CiudadB"

    csv_bytes = facultades_to_csv([f1, f2])
    csv_text = csv_bytes.decode("utf-8")
    lines = csv_text.strip().splitlines()
    assert lines[0] == "id,nombre,abreviatura,ciudad"
    assert "1,Facultad A,FA,CiudadA" in lines[1]
    assert "2,Facultad B,FB,CiudadB" in lines[2]


def test_export_endpoint_integration(client):
    # crear registros en la BD
    from app.models.facultad import Facultad as FacultadModel
    a = FacultadModel(nombre="Fac A", abreviatura="FA", directorio="dir", sigla="S", codigo_postal="1000", ciudad="C1", domicilio="dom", telefono="t", contacto="c", email="a@example.com")
    b = FacultadModel(nombre="Fac B", abreviatura="FB", directorio="dir", sigla="S", codigo_postal="2000", ciudad="C2", domicilio="dom", telefono="t", contacto="c", email="b@example.com")
    db.session.add(a)
    db.session.add(b)
    db.session.commit()

    resp = client.get('/api/v1/facultades/export?format=csv')
    assert resp.status_code == 200
    assert resp.content_type.startswith('text/csv')
    text = resp.data.decode('utf-8')
    assert 'id,nombre,abreviatura,ciudad' in text
    assert 'Fac A' in text and 'Fac B' in text
