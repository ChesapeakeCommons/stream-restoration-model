#!/usr/bin/env python

import os

from flask import request

from . import db
from . import flask
from . import imp
from . import logger


class Application(object):

    def __init__(self, environment, name, extensions=None):
        """Application Constructor.

        Setup our base Flask application, retaining it as our application
        object for use throughout the application.

        :param (class) self
            The representation of the instantiated Class Instance
        :param (str) name
            The name of the application.
        :param (str) environment
            The name of the environment in which to load the application.
        """

        self.name = name
        self.environment = environment
        self.extensions = extensions

        # Create base Flask application.

        self.app = flask.Flask(__name__, static_folder='static')

        # Import custom app configurations.

        self.app.config.from_object(('app.config.%s') % (environment))

        # Set up Cross-Origin Resource Sharing (CORS) rules.

        self.app.after_request(self.setup_cors)

        # Load system modules.

        self.load_modules()

        # Set up database.

        self.setup_database()

    def setup_cors(self, response):
        """Define global Cross-Origin Resource Sharing rules.

        Set header values from application configuration.

        :param (object) self
            the current class (i.e., Application)

        @return (object) response
            the fully qualified response object
        """

        _origin = None

        request_origin = flask.request.headers.get('Origin', '')

        if request_origin in self.app.config['ACCESS_CONTROL_ALLOW_ORIGIN']:

            _origin = request.headers.get('Origin', '')

        # Access-Control-Allow-Methods

        _methods = self.app.config['ACCESS_CONTROL_ALLOW_METHODS']

        # Access-Control-Allow-Headers

        _headers = self.app.config['ACCESS_CONTROL_ALLOW_HEADERS']

        # Access-Control-Allow-Credentials

        _credentials = self.app.config['ACCESS_CONTROL_ALLOW_CREDENTIALS']

        response.headers['Access-Control-Allow-Origin'] = _origin
        response.headers['Access-Control-Allow-Methods'] = _methods
        response.headers['Access-Control-Allow-Headers'] = _headers
        response.headers['Access-Control-Allow-Credentials'] = _credentials

        return response

    def setup_database(self):
        """Setup all database schemas."""
        logger.info('Application is setting up database')

        db.init_app(self.app)
        db.app = self.app

        db.create_all()

    def load_modules(self):
        """Load all application modules.

        Open the module path defined in the configuration, for each module
        directory found in the defined module path we need to `load_module`,
        and create a Flask Blueprint with the module information.

        :param (object) self
            the current class (i.e., Application)
        """
        logger.info('Application beginning to load modules')

        logger.info('Application config: %s', self.app.config)

        modules_path = self.app.config['MODULE_PATH']
        modules_directory = os.listdir(modules_path)

        modules_list = {}

        for module_name in modules_directory:

            module_path = os.path.join(modules_path, module_name)

            if os.path.isdir(module_path):

                try:

                    file_, pathname, descr = imp.find_module(
                        module_name,
                        [modules_path]
                    )

                    modules_list[module_name] = imp.load_module(
                        module_name,
                        file_,
                        pathname,
                        descr
                    )

                except ImportError:

                    logger.error(
                        'Unable to locate the `__init__.py`'
                        ' file in your %s module.' % module_name
                    )
                    
                    raise

                # Register module as Flask blueprint.

                if hasattr(modules_list[module_name], 'module'):

                    module_blueprint = modules_list[module_name].module

                    self.app.register_blueprint(module_blueprint)

                    logger.info(
                        'Application successfully loaded `%s` module.' %
                        module_name
                    )

                else:

                    logger.error(
                        'Application failed to load `%s` module.' %
                        module_name
                    )
