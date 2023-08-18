# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import datetime
import decimal
import logging
import os
import sys
from inspect import getmembers
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask import make_response, jsonify
from flask import session
from flask.blueprints import Blueprint
from flask.cli import click
from flask.json.provider import DefaultJSONProvider

import api.views.entry
from api.extensions import (
    bcrypt,
    cors,
    cache,
    db,
    login_manager,
    migrate,
    celery,
)
from api.models.account import User

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
API_PACKAGE = "api"


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User(user_id, session.get('CAS_USERNAME'), session.get('acl', {}).get('name'))


class ReverseProxy(object):
    """Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


class MyJSONEncoder(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, (decimal.Decimal, datetime.date, datetime.time)):
            return str(o)

        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')

        return o


def create_acl_app(config_object="settings"):
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    register_extensions(app)

    return app


def create_app(config_object="settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])

    app.config.from_object(config_object)
    app.json = MyJSONEncoder(app)
    configure_logger(app)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)
    app.wsgi_app = ReverseProxy(app.wsgi_app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    celery.conf.update(app.config)


def register_blueprints(app):
    for item in getmembers(api.views.entry):
        if item[0].startswith("blueprint") and isinstance(item[1], Blueprint):
            app.register_blueprint(item[1])


def register_error_handlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        import traceback
        app.logger.error(traceback.format_exc())
        error_code = getattr(error, "code", 500)
        if not str(error_code).isdigit():
            error_code = 400
        if error_code != 500:
            return make_response(jsonify(message=str(error)), error_code)
        else:
            return make_response(jsonify(message=traceback.format_exc(-1)), error_code)

    for errcode in app.config.get("ERROR_CODES") or [400, 401, 403, 404, 405, 500, 502]:
        app.errorhandler(errcode)(render_error)

    app.handle_exception = render_error


def register_shell_context(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    for root, _, files in os.walk(os.path.join(HERE, "commands")):
        for filename in files:
            if not filename.startswith("_") and filename.endswith("py"):
                module_path = os.path.join(API_PACKAGE, root[root.index("commands"):])
                if module_path not in sys.path:
                    sys.path.insert(1, module_path)
                command = __import__(os.path.splitext(filename)[0])
                func_list = [o[0] for o in getmembers(command) if isinstance(o[1], click.core.Command)]
                for func_name in func_list:
                    app.cli.add_command(getattr(command, func_name))


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(pathname)s %(lineno)d - %(message)s")

    if app.debug:
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    log_file = app.config['LOG_PATH']
    file_handler = RotatingFileHandler(log_file,
                                       maxBytes=2 ** 30,
                                       backupCount=7)
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
