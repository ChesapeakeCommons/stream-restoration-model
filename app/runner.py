#!/usr/bin/env python


def create_production_application():

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
