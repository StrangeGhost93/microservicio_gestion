from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_hashids import Hashids


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
hashids = Hashids()
