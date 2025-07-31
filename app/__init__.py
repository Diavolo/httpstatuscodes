from http import HTTPStatus
import os

from dotenv import load_dotenv
from flask import Flask, render_template
import sentry_sdk

from app.routes.home import home
from app.routes.api import api
from app.utils.constants import NOT_FOUND_HTML_TEMPLATE, SERVER_ERROR_HTML_TEMPLATE


load_dotenv()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    is_production = os.getenv("FLASK_ENV") == "production"

    if is_production:
        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            send_default_pii=True,
        )

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=error
        ), HTTPStatus.NOT_FOUND

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template(
            SERVER_ERROR_HTML_TEMPLATE, error_message=error
        ), HTTPStatus.INTERNAL_SERVER_ERROR

    app.register_blueprint(api)
    app.register_blueprint(home)

    return app
