from io import StringIO
import csv
from typing import Iterable


def facultades_to_csv(facultades: Iterable[object]) -> bytes:
    """Convierte una lista de objetos Facultad a CSV (bytes).

    Columnas: id,nombre,abreviatura,ciudad
    """
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "nombre", "abreviatura", "ciudad"])
    for f in facultades:
        writer.writerow([
            getattr(f, "id", ""),
            getattr(f, "nombre", ""),
            getattr(f, "abreviatura", ""),
            getattr(f, "ciudad", ""),
        ])
    return output.getvalue().encode("utf-8")
