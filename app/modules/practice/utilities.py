#!/usr/bin/env python

"""Modules package.

Created by Viable Industries, L.L.C. on 01/26/2015.
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

import json
from datetime import datetime

# Import Flask dependencies

from flask import abort
from flask import request

# Import third-party dependencies

from werkzeug.datastructures import MultiDict
from werkzeug.datastructures import ImmutableMultiDict

from sqlalchemy import desc

# Import package dependencies

from app import db
from app import logger
from app import serializer
from app import utilities

from app.schema.practice import Practice


def extract_tokens(data, key):

    tokens = data.get(key, '').split(',')

    if tokens:

        try:

            return [int(datum) for datum in tokens]

        except (TypeError, ValueError):

            pass

    raise ValueError('Invalid query parameter.')


def _build_boolean_filters(params):

    if not params:

        return None

    _boolean_filters = []

    for parameter in ['organization', 'program', 'tag']:

        try:

            domain = extract_tokens(params, parameter)

            logger.debug(
                'practice._build_boolean_filters.domain: %s',
                domain)

            if domain:

                FILTER_MAP[parameter](_boolean_filters, domain)

        except ValueError:

            pass

    return _boolean_filters


def _build_filters(params=None):

    logger.debug(
        'practice._build_filters.params: %s',
        params)

    logger.debug(
        'practice._build_filters.params: %s',
        type(params))

    _filters = []

    if params and isinstance(params, (dict, MultiDict, ImmutableMultiDict)):

        logger.debug(
            'practice._build_filters: `params` arg is valid')

        _boolean_filters = _build_boolean_filters(params)

        _filters.append(
            db.or_(*_boolean_filters)
        )

    return _filters


def get_collection():

    _filters = _build_filters(request.args)

    logger.debug('Practice filters: %s', str(_filters))

    _sort_param = utilities.parse_query_sort(Practice, request.args)

    try:

    	_page = int(request.args.get('page', 1))

    except (TypeError, ValueError):

    	abort(400, 'Invalid `page` parameter.')

    _limit = utilities.parse_query_limit(request.args)

    _query = db.session.query(
        Practice
    ).filter(
        *_filters
    ).order_by(
        _sort_param
    ).limit(
        _limit
    ).offset(
    	(_page - 1) * _limit
    )

    if request.args.get('minimal') == 'true':

        columns = Practice.__table__.columns.keys()

        _excluded_attrs = [
            column for column in columns
            if column not in ['id', 'name', 'target']
        ]

    else:

        _excluded_attrs = utilities.get_excluded_attrs(request.args)

    return [
        serializer.compose_feature(
            result, [], _excluded_attrs)
        for result in _query
    ]
