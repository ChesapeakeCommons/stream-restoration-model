#!/usr/bin/env python

"""Define the FieldDoc application.

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

# Import standard dependencies

import argparse
import flask
import imp
import logging
import os

# Import Flask dependencies

from flask.ext.sqlalchemy import SQLAlchemy

# Import third-party dependencies

from celery import Celery

# Import package dependencies

from . import responses


"""Setup Celery"""
celery = Celery(__name__)


"""System Logging.

System logging enables us to retain useful activity within the system in
server logs. Log messages are written to the Terminal or Application Runner
(e.g., Supervisor) server logs.

Below sets up the `basicConfig` which opens a stream that allows us to add
formatted log messages to the root logger.

@param (object) logger
    Provides the ability to write directly to the logger with the info(),
    warning(), error(), and critical() methods

See the official Python::logging documentation for more Information
https://docs.python.org/2/library/logging.html
"""
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


responses = responses.Responses()


"""Meta Information.
"""
__author__ = 'Joshua I. Powell'
__copyright__ = 'Copyright 2016 Viable Industries, L.L.C. All rights reserved.'
__date__ = '2015-12-27'
__license__ = 'Proprietary'
__organization__ = 'Viable Industries, L.L.C.'
__status__ = 'Development'
__version__ = '0.0.1'


"""Production Application Runner.
"""
def create_application():

    from . import application
    from . import errors

    """Instantiate the Application

    Setup the basic Application class in order to instantiate the rest of
    the Application

    @param (str) name
        The name of the Application
    @param (str) envioronment
        The desired environment configuration to start the application on
    """
    instance = application.Application(
        name="__main__",
        environment='production.ProductionConfig'
    )

    """Instaniate App-level error handling

    :param object app: Instantiated app object
    """
    errors = errors.ErrorHandlers(instance.app)
    errors.load_errorhandler(instance.app)

    return instance.app
