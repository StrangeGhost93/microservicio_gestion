from app import create_app
from flask_migrate import Migrate
from app import db
import logging
# Ref: https://docs.python.org/3/library/logging.html
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


# funcion en __init__.py que devuelve una instancia de la app Flask.
app = create_app()


if __name__ == '__main__':
    # arranca el servidor Flask localhost:5000
    app.run(host="0.0.0.0", debug=True, port=5000)

migrate = Migrate(app, db)    