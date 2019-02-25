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


from flask import abort
from flask import jsonify


from app import oauth
from app.permissions import *


from . import module
from . import Model
from app.schema.practice import Practice

@module.route('/v1/data/summary/bank-stabilization/<int:practice_id>', methods=['OPTIONS'])
def summary_bankstabilization_options(practice_id):
    """Define default user preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })

@module.route('/v1/data/summary/bank-stabilization/<int:practice_id>', methods=['GET'])
@oauth.require_oauth()
def summary_bankstabilization_get(oauth_request, practice_id):
    """Define default user request."""
    authorization = oauth_request.user

    if not hasattr(authorization, 'id'):
        abort(403)

    resource = Practice.query.get(practice_id)

    if check_roles('grantee', authorization.roles):
        if (authorization.id == resource.creator_id) or \
           (is_group_member(authorization.id, resource.site.project.members) or \
           (resource.site.project.creator_id == authorization.id) or \
           (resource.site.creator_id == authorization.id)):
            """User.grantee may only see Practice if...

            - They are the creator of the Practice
            - They belong to the Project.members that this practice
              belongs to
            """
            pass
        else:
            logger.warning('User %d %s access failed Bank Stabilization '
                           'Summary' % (authorization.id,
                                           'grantee'))
            abort(401)
    elif check_roles('manager', authorization.roles):
        if is_account_manager(resource.site.project.account_id,
                              authorization.account):
            logger.info('User %s access resource %s' %
                        (authorization.id, practice_id))
            pass
        else:
            logger.warning('User %d %s access failed Bank Stabilization'
                           'Summary' %
                           (authorization.id, 'manager'))
            abort(401)
    elif check_roles('admin', authorization.roles):
        logger.info('User %d accessed Practice as %s' %
                    (authorization.id, 'admin'))
        pass
    else:
        logger.info('User %d accessed Bank Stabilization Summary with no '
                    'role' %
                    (authorization.id))
        abort(403)

    """If method has reached this point the user is allowed to access this
    particluar Summary."""
    _model = Model()
    _summary = _model.get_summary(practice_id)

    return jsonify(**_summary), 200
