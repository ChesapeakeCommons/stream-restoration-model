"""Define the class for creating our application.

Created by Viable Industries, L.L.C. on 12/27/2015.
Copyright 2016 Viable Industries, L.L.C. All rights reserved.

For license and copyright information please see the LICENSE document (the
"License") included with this software package. This file may not be used
in any manner except in compliance with the License unless required by
applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""

import os

# Import standard dependencies

from datetime import datetime

# Import Flask dependencies

from flask import jsonify
from flask import request
from flask.ext.restless import APIManager
from flask.ext.security.signals import user_registered

# Import package dependencies

from . import db
from . import celery
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

        self.init_celery()

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


    def init_celery(self):
        
        celery.conf.result_backend = self.app.config['CELERY_BACKEND']
        celery.conf.broker_url = self.app.config['CELERY_BROKER']

        celery.conf.update(self.app.config)

        celery.app = self.app


    def assign_default_user_role(self, app, db, user_datastore, role):
        """Ensure that users are assigned the app-defined role by default.

        :param object app
            the application we are acting upon
        :param object db
            the database our application is using for storage
        :param object user_datastore
            the Flask Security User Datastore implementation
        :param string role
            the name of the `Role` we want to assign by default
        """
        @user_registered.connect_via(app)
        def user_registered_sighandler(app, user, confirm_token):

            """Retrieve the default role requested."""
            default_role = user_datastore.find_role(role)

            """Assign that role to the acting `User` object."""
            user_datastore.add_role_to_user(user, default_role)

            """Save all of our revisions to the database."""
            db.session.commit()


    def load_endpoint(self, Module):
        r"""Load a single module endpoint.

        Given a module name, locate the `endpoint.py` file, and instantiate a
        new Flask Restless compatible endpoint accorindg to the settings
        contained within the `endpoint.py` file.

        :param object self: The Application class
        :param object Module: The of module containing endpoint

        See the official Flask Restless documentation for more information
        https://flask-restless.readthedocs.org/en/latest/api.html#\
        flask.ext.restless.APIManager.create_api
        """
        manager = APIManager(self.app, flask_sqlalchemy_db=db)

        if hasattr(Module, 'endpoints'):
            if hasattr(Module, 'Model'):
                Seed_ = Module.endpoints.Seed()
                manager.create_api(Module.Model, **Seed_.__arguments__)
                logger.info('`%s` module endpoints loaded' %
                            (Module.__name__))
            else:
                logger.error('`%s` module has endpoints, but is missing '
                             'Model' % (Module.__name__))
        else:
            logger.info('`%s` module did not contain any endpoints.' %
                        (Module.__name__))


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

                    """Load any endpoints that are contained within this module.

                    Use the Application.load_endpoint method to instantiate any
                    endpoints contained within the module.
                    """
                    self.load_endpoint(modules_list[module_name])
                else:
                    logger.error('Application failed to load `%s` module' %
                                 (module_name))
