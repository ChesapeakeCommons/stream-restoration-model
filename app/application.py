#!/usr/bin/env python

import os
from datetime import datetime

from flask import request

from . import db
from . import flask
from . import imp
from . import logger
from . import os


class Application(object):
    """Create Flask Application via a Class."""

    def __init__(self, environment, name, app=None, extensions={}):
        """Application Constructor.

        Setup our base Flask application, retaining it as our application
        object for use throughout the application

        :param (class) self
            The representation of the instantiated Class Instance
        :param (str) name
            The name of the application
        :param (str) environment
            The name of the enviornment in which to load the application
        :param (class) app
            The Flask class for the application that was created
        """
        logger.info('Application Started at %s', datetime.utcnow())

        logger.info('Application environment: %s', environment)

        self.name = name
        self.environment = environment
        self.extensions = extensions

        """Create our base Flask application
        """
        self.app = flask.Flask(__name__, static_folder='static')

        """Import all custom app configurations
        """
        self.app.config.from_object(('app.config.%s') % (environment))

        logger.info('Application config: %s', self.app.config)

        """Setup Cross Site Origin header rules
        """
        self.app.after_request(self.setup_cors)

        """Load system extensions
        """
        self.load_extensions()

        """Load system modules
        """
        self.load_modules()

        """Setup the Database
                """
        self.setup_database()

        logger.info('Application setup complete')

    def setup_cors(self, response):
        """Define global Cross Origin Resource Sharing rules.

        Setup our headers so that the respond correctly and securely

        :param (object) self
            the current class (i.e., Application)

        @return (object) response
            the fully qualified response object
        """
        logger.info('Application Cross Origin Resource Sharing')

        """Access-Control-Allow-Origin
        """
        _origin = None

        if flask.request.headers.get('Origin', '') in \
                self.app.config['ACCESS_CONTROL_ALLOW_ORIGIN']:
            _origin = request.headers.get('Origin', '')

        """Access-Control-Allow-Methods
        """
        _methods = self.app.config['ACCESS_CONTROL_ALLOW_METHODS']

        """Access-Control-Allow-Headers
        """
        _headers = self.app.config['ACCESS_CONTROL_ALLOW_HEADERS']

        """Access-Control-Allow-Credentials
        """
        _credentials = self.app.config['ACCESS_CONTROL_ALLOW_CREDENTIALS']

        """Setup Access Control headers for the application

        Using the user defined enviornment, setup access control headers
        """
        response.headers['Access-Control-Allow-Origin'] = _origin
        response.headers['Access-Control-Allow-Methods'] = _methods
        response.headers['Access-Control-Allow-Headers'] = _headers
        response.headers['Access-Control-Allow-Credentials'] = _credentials

        return response

    def load_extensions(self):
        """Define reusable extensions throughout the main application.

        Setup system extensions that are critical to the secure operation of
        this application

        :param (object) self
            the current class (i.e., Application)
        """
        logger.info('Application is setting up database')

    def setup_database(self):
        """Setup all database schemas."""
        logger.info('Application is setting up database')

        """Setup the database and associate it with the application
        """
        db.init_app(self.app)
        db.app = self.app

        """Create all database tables

        Create all of the database tables defined with the modules
        """
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
            module_package = os.path.join(modules_path, module_name,
                                          '__init__.py')

            if os.path.isdir(module_path):

                """Locate and load the module into our module_list
                """
                try:

                    f, filename, descr = imp.find_module(module_name,
                                                         [modules_path])
                    modules_list[module_name] = imp.load_module(module_name,
                                                                f, filename,
                                                                descr)
                except ImportError:

                    logger.error('`load_modules` was unable to locate the'
                                 '`__init__.py` file in your %s module' %
                                 (module_name))
                    
                    raise

                """Register this module with the application as a blueprint

                See the official Flask API for more information about Blueprint
                http://flask.pocoo.org/docs/0.10/api/#flask.Flask.register_blueprint
                """
                if hasattr(modules_list[module_name], 'module'):

                    module_blueprint = modules_list[module_name].module
                    self.app.register_blueprint(module_blueprint)

                    logger.info('Application successfully loaded `%s` module' %
                                (module_name))

                else:

                    logger.error('Application failed to load `%s` module' %
                                 (module_name))
