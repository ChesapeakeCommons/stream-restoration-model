#!/usr/bin/env python

"""Geography Views.

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

# Import module dependencies

from . import module
from . import utilities


@module.route('/v1/geographies', methods=['OPTIONS'])
def geography_collection_options():

    """Define default user preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/geographies', methods=['GET'])
def geography_collection_get():

    _features = utilities.get_collection()

    return jsonify(**{
        'features': _features
    }), 200


@module.route('/v1/geography/<int:feature_id>', methods=['OPTIONS'])
def geography_options(feature_id):

    """Define default user preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/geography/<int:feature_id>', methods=['GET'])
def geography_get(feature_id):

    _feature = utilities.get_feature(feature_id)

    return jsonify(**_features), 200


@module.route('/v1/geography/<int:feature_id>/tasks', methods=['OPTIONS'])
def geography_tasks_options(feature_id):

    """Define default user preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/geography/<int:feature_id>/tasks', methods=['GET'])
def geography_tasks_get(feature_id):

    _tasks = utilities.get_tasks()

    return jsonify(**{
        'features': _tasks
    }), 200
