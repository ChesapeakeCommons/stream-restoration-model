"""

  FieldDoc_test.py
  FieldDoc::Tests

  Created by Viable Industries, L.L.C. on 12/27/15.
  Copyright 2016 Viable Industries, L.L.C. All rights reserved.

"""


"""
Import Package Dependencies
"""
from . import TestCase
from . import Flask


"""
Import Application Dependencies
"""
from app.application import Application
from app.application_arguments import ApplicationArguments


"""
Base FieldDoc Testing Suite
"""
class FieldDocTest(TestCase):

    """
    Setup class for testing
    """
    def setUp(self):

        self.arguments = ApplicationArguments()

        self.instance = Application(
            name = __name__,
            environment = 'testing.TestingConfig'
        )


    """
    Test: Result should return a Flask Class meaning that we have properly
          instantiated the Flask application
    """
    def test_FieldDocIsFlaskApp(self):

        self.assertIsInstance(self.instance.app, Flask)


    """
    Test: Result should return a ApplicationArguments Class meaning that we
          have properly loaded the argument parser into the application.
    """
    def test_FieldDocHasArgumentParser(self):

        self.assertIsInstance(self.arguments, ApplicationArguments)
