import os
import logging
from flask import Flask, redirect, url_for
from bank.index import index_bp
from bank.auth import auth_bp
from bank.extensions import bootstrap, db, login_manager
from bank.transaction import tranx_bp


def create_app(config_name="config.py"):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('bank')
    app.config.from_pyfile(config_name)
    register_extensions(app)
    register_blueprints(app)
    setup_logging()
    return app


def register_extensions(app):
    """
    Register external components like databases to the `Flask` app instance.
    :param app:
    :return: Flask.app
    """
    bootstrap.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def register_blueprints(app):
    """
    Register all routes to the app instance.
    :param app:
    :return: Flask.app
    """
    app.register_blueprint(index.index_bp)
    app.register_blueprint(tranx_bp)
    app.register_blueprint(auth.auth_bp)


@login_manager.unauthorized_handler
def unauthorized():
    """

    :return:
    """
    return redirect(url_for('auth.login'))



app = create_app()
