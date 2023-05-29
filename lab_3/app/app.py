'''
Файл створення Flask-застосунку'''

import os
import redis
import logging
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


MIGRATIONS_DIRECTORY = os.path.join("migrations")

USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
DB = os.environ["DB"]

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]

db = SQLAlchemy()
migrate = Migrate(directory=MIGRATIONS_DIRECTORY)
logger = logging.getLogger("app.manual")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Local Test
# r = redis.Redis(host='cache', port='6379')

def create_app():
    app = Flask(__name__)
    app.config.from_mapping({
        "SQLALCHEMY_DATABASE_URI": f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DB}"})

    # Local Test
    # app.config.from_mapping({
    #     "SQLALCHEMY_DATABASE_URI": f"postgresql+psycopg2://postgres:postgres@localhost/zno"})

    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    app.register_blueprint(views.person.bp)
    app.register_blueprint(views.test.bp)
    app.register_blueprint(views.query.bp)
    
    @app.route("/", methods=["GET", "POST"])
    def rootredirect():
        return redirect(url_for("person.person_all_desc"))

    return app