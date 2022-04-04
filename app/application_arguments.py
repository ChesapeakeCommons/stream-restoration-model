#!/usr/bin/env python

from . import argparse


class ApplicationArguments(object):
    """Command Line Interface.

    Setup named application arguments and command line interface help
    information.

    @param (class) self
        The representation of the instantiated Class Instance
    @param (class) parser
        The name of the application
    @param (class) args
        The name of the enviornment in which to load the application
    """

    def __init__(self, parser=None, args=None):
        """Command Line Interface constructor.

        @param (object) self
        @param (object) parser
        @param (object) args
        """
        self.parser = argparse.ArgumentParser(**{
            'prog': 'FieldDoc',
            'description': 'The FieldDoc Core API service'
        })

        self.parser.add_argument('--environment', **{
            'type': str,
            'help': 'set application environment (default: testing)',
            'default': 'testing'
        })

        self.parser.add_argument('--host', **{
            'type': str,
            'help': 'set hostname to listen on (default: 127.0.0.1)',
            'default': '127.0.0.1'
        })

        self.parser.add_argument('--port', **{
            'type': int,
            'help': 'set port of webserver (default: 5000)',
            'default': 5000
        })

        self.parser.add_argument('--debug', **{
            'type': bool,
            'help': 'enable or disable debug mode (default: False)',
            'default': False
        })

        self.args = self.parser.parse_args()
