#!/usr/bin/env python

"""Summary Views.

Created by Viable Industries, L.L.C. on 10/17/2017.
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

# Import Flask dependencies

from flask import abort
from flask import jsonify
from flask import request

# Import module dependencies

from . import module
from . import Model
from . import utilities


@module.route('/v1/analyze', methods=['OPTIONS'])
def analyze_options():

    """Define default user preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/analyze', methods=['POST'])
def analyze_post():

    datum = utilities.handle_request(
        request.get_json())

    return jsonify(**datum), 200


@module.route('/v1/analyze/<practice_type>', methods=['OPTIONS'])
def analyze_type_options():

    """Define default user preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/analyze/<practice_type>', methods=['POST'])
def analyze_type_post(practice_type):

    datum = utilities.handle_request(
        practice_type,
        request.get_json())

    return jsonify(**datum), 200
