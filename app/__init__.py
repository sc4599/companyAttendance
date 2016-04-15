
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from attendance.forms import FileUploadForm
from flask.ext.sqlalchemy import SQLAlchemy

import config

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
    app.config['ALLOWED_EXTENSIONS'] = set(['xls'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'songchao'

    bootstrap.init_app(app)
    db.init_app(app)
    return app



