#!/usr/bin/env python

"""Start the application.

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


from app import application
from app import application_arguments as args
from app import errors


if __name__ == "__main__":
    """Instantiate the Application Arguments.

    Setup the Application Arguments in order to pass user defined command
    line interface arguments to the Application

    @param None
    """
    arguments = args.ApplicationArguments()

    """Instantiate the Application

    Setup the basic Application class in order to instantiate the rest of
    the Application

    @param (str) name
        The name of the Application
    @param (str) envioronment
        The desired environment configuration to start the application on
    """
    instance = application.Application(
        name=__name__,
        environment=arguments.args.environment
    )

    """Instaniate App-level error handling

    :param object app: Instantiated app object
    """
    # instance.load_errorhandler(instance.app)
    errors = errors.ErrorHandlers(instance.app)
    errors.load_errorhandler(instance.app)

    """Run the application.

    Run the application with the given variables

    @param (str) host
        The hostname to listen on
    @param (int) port
        The port of the webserver
    @param (bool) debug
        Enable or disable debug mode
    @param (dict) **options
        Options to be forwarded to the underlying Werkzeug server

    @see http://werkzeug.pocoo.org/docs/0.11/serving/\
            #werkzeug.serving.run_simple
    """
    instance.app.run(host=arguments.args.host, port=arguments.args.port,
                     debug=arguments.args.host)
