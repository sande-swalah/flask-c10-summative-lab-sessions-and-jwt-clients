from flask import Flask

from app.config import Config, bcrypt, db, migrate
from app.controllers.routes import register_routes


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    register_routes(app)

    return app


app = create_app()
