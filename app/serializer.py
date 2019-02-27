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

# Import third-party dependencies

import geoalchemy2.functions as geofunc
from geoalchemy2.elements import WKBElement

# Import package dependencies

from app import logger


def _parse_value(key, value, obj=None):

    logger.debug('_parse_value.key: %s', key)
    logger.debug('_parse_value.value: %s', value)
    logger.debug('_parse_value.obj: %s', obj)

    if isinstance(value, datetime):

        return value.isoformat()

    if obj and value and key.endswith('_id'):

        return _dict_copy(
            getattr(obj, _parse_key(key)),
            shallow=True)

    return value


def _parse_key(obj):

    if obj.endswith('_id'):

        return obj.replace('_id', '')

    return obj


def _parse_relation(relation, exclude_columns=None):

    if relation:

        if isinstance(relation, list):

            _copy = []

            for item in relation:

                _copy.append(_dict_copy(
                    item,
                    shallow=True,
                    exclude_columns=exclude_columns))

            return _copy

        return _dict_copy(
            relation,
            shallow=True,
            exclude_columns=exclude_columns)

    return None


def _dict_copy(obj, shallow=False, exclude_columns=None):

    # TODO: Support nested attributes using dot notation.

    # import operator
    # operator.attrgetter("b.c")(a)

    logger.debug(
        'app.serializer._dict_copy.exclude_columns: %s',
        exclude_columns)

    _excluded_columns = exclude_columns or []

    _attributes = [key for key in obj.__table__.columns.keys()
                   if key not in _excluded_columns]

    logger.debug('app.serializer._dict_copy._attributes: %s', _attributes)

    if shallow:

        return {_parse_key(key): _parse_value(key, getattr(obj, key))
                for key in _attributes}

    return {_parse_key(key): _parse_value(key, getattr(obj, key), obj)
            for key in _attributes}


def minimal_copy(obj, reserved=None):

    logger.debug(
        'app.serializer.minimal_copy.obj: %s',
        obj)

    logger.debug(
        'app.serializer.minimal_copy.reserved: %s',
        reserved)

    if isinstance(obj, dict):

        try:

            datum = {
                'id': obj.get('id'),
                'name': obj.get('name')
            }

            return datum

        except AttributeError as error:

            raise

    if not reserved:

        reserved = [
            'id',
            'name'
        ]

    _excluded_columns = [
        key for key in obj.__table__.columns.keys()
        if key not in reserved
    ]

    logger.debug(
        'app.serializer.minimal_copy._excluded_columns: %s',
        _excluded_columns)

    return _dict_copy(
        obj,
        shallow=True,
        exclude_columns=_excluded_columns)


def compose_feature(obj, recurse_on=None, exclude_columns=None):

    logger.debug(
        'app.serializer.compose_feature.obj: %s',
        obj)

    logger.debug(
        'app.serializer.compose_feature.recurse_on: %s',
        recurse_on)

    logger.debug(
        'app.serializer.compose_feature.exclude_columns: %s',
        exclude_columns)

    _datum = _dict_copy(obj=obj, exclude_columns=exclude_columns)

    for attribute in recurse_on:

        _datum[attribute] = _parse_relation(
            getattr(obj, attribute),
            exclude_columns)

    return _datum
