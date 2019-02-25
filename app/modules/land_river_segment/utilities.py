# #!/usr/bin/env python

# """Modules package.

# Created by Viable Industries, L.L.C. on 01/26/2015.
# Copyright 2016 Viable Industries, L.L.C. All rights reserved.

# For license and copyright information please see the LICENSE document (the
# "License") included with this software package. This file may not be used
# in any manner except in compliance with the License unless required by
# applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.

# See the License for the specific language governing permissions and
# limitations under the License.
# """

# # Import standard dependencies

# import json

# # Import Flask dependencies

# from flask import abort
# from flask import request

# # Import third-party dependencies

# from sqlalchemy import desc
# from sqlalchemy.sql.expression import cast
# from geoalchemy2 import Geometry
# import geoalchemy2.functions as geofunc

# from werkzeug.datastructures import MultiDict
# from werkzeug.datastructures import ImmutableMultiDict

# # Import package dependencies

# from app import db
# from app import logger
# from app import serializer
# from app import utilities

# from app.modules.site.utilities import parse_node

# from app.schema.custom_geography import CustomGeography
# from app.schema.custom_geography import CustomGeographyType
# from app.schema.organization import Organization
# from app.schema.program import Program


# def _build_boolean_filters(params):

#     if not params:

#         return None

#     _boolean_filters = []

#     if params.get('organization', None):

#         _organization_ids = params.get('organization').split(',')

#         _boolean_filters.append(
#             CustomGeography.organization_id.in_(_organization_ids)
#         )

#     if params.get('program', None):

#         _program_ids = params.get('program').split(',')

#         _boolean_filters.append(
#             CustomGeography.program_id.in_(_program_ids)
#         )

#     if params.get('tag', None):

#         _tag_ids = params.get('tag').split(',')

#         _boolean_filters.append(
#             CustomGeography.tags.any(
#                 Tag.id.in_(_tag_ids))
#         )

#     return _boolean_filters


# def _build_filters(user, params, scope='user'):

#     try:

#         scope = params.get('scope')

#     except AttributeError:

#         pass

#     _filters = []

#     # Restrict matches to projects created by
#     # or associated with the `User` instance.

#     if scope == 'all':

#         pass

#     else:

#         # Restrict matches to projects created by
#         # or associated with the `User` instance.

#         _user_filters = [
#             CustomGeography.creator_id == user.id,
#             CustomGeography.organization_id == user.organization_id
#         ]

#         _filters.append(db.or_(*_user_filters))

#     _boolean_filters = _build_boolean_filters(params)

#     if _boolean_filters:

#         _filters.append(
#             db.or_(*_boolean_filters)
#         )

#     return _filters


# def get_collection(user):

#     _filters = _build_filters(user, request.args)

#     logger.debug('Geography filters: %s', _filters)

#     _sort_column = request.args.get('sort', 'modified_on').lower()

#     _limit = utilities.parse_query_limit(request.args)

#     _query = db.session.query(
#         CustomGeography
#     ).filter(
#         *_filters
#     ).order_by(
#         desc(getattr(CustomGeography, _sort_column))
#     ).limit(
#         _limit
#     ).offset(0)

#     logger.debug('Geography query: %s', str(_query))

#     _exclude_geometry = request.args.get('exclude_geometry', False)

#     return [
#         parse_node(node, _exclude_geometry)
#         for node in _query
#     ]


# def delete_collection(user):

#     _program_id = request.args.get('program')

#     _program = db.session.query(
#         Program
#     ).filter(
#         Program.id == _program_id
#     ).first()

#     if _program:

#         _permissions = _program.get_permissions(user)

#         if (_permissions.get('read') and
#             _permissions.get('write')):

#             db.session.query(
#                 CustomGeography
#             ).filter(
#                 CustomGeography.program_id == _program.id
#             ).delete()

#             db.session.commit()

#             return True

#         else:

#             abort(403)

#     else:

#         abort(404)


# def get_feature(feature_id):

#     _node = db.session.query(
#         CustomGeography
#     ).filter(
#         CustomGeography.id == feature_id
#     ).first()

#     if _node:

#         logger.debug('Program geography query: %s', _node)

#         return [parse_node(node) for node in _node.geographies]

#     return []


# def get_tasks(feature_id, user):

#     feature = db.session.query(
#         CustomGeography
#     ).filter(
#         CustomGeography.id == feature_id
#     ).first()

#     if feature:

#         return [
#             serializer.compose_feature(task, ['errors'])
#             for task in feature.tasks
#         ]

#     return []


# def create_group(name):

#     logger.debug('geography.create_group.name: %s', name)

#     _new_group = CustomGeographyType(**{
#         'name': name
#     })

#     db.session.add(_new_group)

#     db.session.flush()

#     return _new_group


# def validate_group(data):

#     if isinstance(data, dict):

#         _group = data.get('category')

#         if isinstance(_group, dict):

#             data['category_id'] = _group.get('id')

#         elif isinstance(_group, basestring):

#             _new_group = create_group(_group)

#             data['category_id'] = _new_group.id

#         #: Having established a valid `TagGroup.id`,
#         #: remove the `group` attribute to prevent
#         #: `AttributeError` thrown by SQLAlchemy.

#         data.pop('category', None)

#     return data
