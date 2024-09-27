from flask import Flask
from flask.logging import default_handler

from app.middlewares.json_provider import AppJSONProvider
from app.utils import logging_utils


def create_app(config='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.json = AppJSONProvider(app)
    app.json.sort_keys = False
    app.logger.removeHandler(default_handler)
    logging_utils.setup_logging()

    # Load configuration
    app.config.from_object(config)

    # Register error handler
    from .middlewares import error_handler, request_id_loader
    error_handler.init_app(app)
    request_id_loader.init_app(app)

    # Register database

    from .database import db
    db.init_app(app)

    # Register blueprints
    from app.routes import api
    from app.routes.user_routes import user_bp

    api.register_blueprint(user_bp, url_prefix="/users")  # child blueprint(s)
    app.register_blueprint(api, url_prefix='/api')  # parent blueprint

    return app
