#!/usr/bin/env python

"""Define the FieldDoc Endpoint Class.

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

from werkzeug.exceptions import BadRequestKeyError
from oauthlib.oauth2 import InvalidScopeError
from sqlalchemy.exc import ProgrammingError
from psycopg2 import IntegrityError

# Import package dependencies

from app import logger
from app import responses


class ErrorHandlers(object):
    """Error handling for this Flask Application.

    :param object object: For a full explanation please see
    https://docs.python.org/release/2.2.3/whatsnew/sect-rellinks.html

    See the official Flask API documnetation for more information
    http://flask.pocoo.org/docs/0.10/patterns/errorpages/#error-handlers
    """

    def __init__(self, app):
        """Initialize all top level variables."""
        self.app = app

    def __repr__(self):
        """Display of ErrorHandler when inspected."""
        return '<ErrorHandler SystemVI>'

    def find_message(self, error):
        """Verify that error block has description.

        If no error.description exists then we need to return an empty string

        :param object error: The error object we wish to inspect

        :return string message: The message string produced by method
        """
        message = ''

        if hasattr(error, 'description'):
            message = error.description

        return message

    def load_errorhandler(self, app):
        """Define error handling responses for the application.

        See the official Flask API documentation for more information
        http://flask.pocoo.org/docs/0.10/api/#flask.Flask.errorhandler
        """
        @app.errorhandler(400)
        # @app.errorhandler(Exception)
        @app.errorhandler(BadRequestKeyError)
        @app.errorhandler(ProgrammingError)
        @app.errorhandler(IntegrityError)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)

            return responses.status_400(message), 400

        @app.errorhandler(401)
        # @app.errorhandler(Exception)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)

            return responses.status_401(message), 401

        @app.errorhandler(403)
        # @app.errorhandler(Exception)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)

            return responses.status_403(message), 403

        @app.errorhandler(404)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)

            return responses.status_404(message), 404

        @app.errorhandler(405)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)

            return responses.status_405(message), 405

        @app.errorhandler(410)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)

            return responses.status_410(message), 410

        @app.errorhandler(500)
        @app.errorhandler(InvalidScopeError)
        def internal_error(error):
            logger.error('ErrorHandler Exception %s', error)

            message = self.find_message(error)

            return responses.status_500(message), 500
