#!/usr/bin/env python

__author__ = 'Brendan McIntyre'
__copyright__ = 'Copyright 2022 The Commons. All rights reserved.'
__date__ = '2022-04-04'
__license__ = 'Proprietary'
__organization__ = 'The Commons'
__status__ = 'Development'
__version__ = '0.0.1'

import argparse
import flask
import imp
import logging
import os

from flask.ext.sqlalchemy import SQLAlchemy

from . import responses


"""Setup Database.

Initializes the object relational mapper (ORM) that allows the application to
communicate directly with the database.

@param (object) db
    The instantiated SQLAlchemy instance

See the official SQLAlchemy documentation for more information
http://docs.sqlalchemy.org/en/latest/
"""
db = SQLAlchemy(session_options={"autoflush": False})

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

responses = responses.Responses()


def create_application():

    from . import application
    from . import errors

    instance = application.Application(
        name='__main__',
        environment='production.ProductionConfig'
    )

    errors = errors.ErrorHandlers(instance.app)
    errors.load_errorhandler(instance.app)

    return instance.app
