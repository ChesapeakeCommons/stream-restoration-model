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

from app import application
from app import errors


"""Production Application Runner.
"""
def create_production_application():

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
