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

# import inspect
import json
import math
import re
import time
from datetime import datetime
from decimal import Decimal

# Import third-party dependencies

from geoalchemy2 import Geometry
import geoalchemy2.functions as geofunc
from geoalchemy2.elements import WKBElement
from sqlalchemy import desc
from sqlalchemy import inspect
from sqlalchemy.sql.expression import cast

# Import Flask dependencies

from flask import current_app
from flask import render_template

from flask.ext.mail import Message

from werkzeug.local import LocalProxy
from werkzeug.datastructures import MultiDict
from werkzeug.datastructures import ImmutableMultiDict

# Import package dependencies

from app import logger
from app import serializer

from app.geometry import ST_MakeEnvelope
from app.geometry import ST_GeomFromGeoJSON


def unix_time(obj):
    """
    Represent a datetime object in milliseconds
    since the Unix epoch (1970-01-01 00:00:00).

    :param obj: A datetime object. Note that no
    support is provided for time zones. Stored
    values throughout the system follow the UTC
    standard.
    """

    epoch = datetime.utcfromtimestamp(0)

    return int((obj - epoch).total_seconds()) * 1000


def display_date(date_string):

    """
    Convert date string to conventional format

    e.g. 2017-09-20 --> September 20, 2017

    Args:
        date_string (str): String representing a date.
    """

    tpl = '%Y-%m-%d'

    if 'T' in date_string:

        tpl = '%Y-%m-%dT%H:%M:%S'

    if '.' in date_string:

        tpl = '%Y-%m-%dT%H:%M:%S.%f'

    struct_time = time.strptime(date_string, tpl)

    # Convert struct_time to datetime object

    date_time = datetime.fromtimestamp(time.mktime(struct_time))

    return date_time.strftime('%b %d, %Y')


def normalize_string(text=None):

    """
    Remove all non-alphanumeric chars from the input string.

    Apply str.lower() and str.strip() before executing re.sub().
    """

    if text:

        _text = '_'.join(text.lower().strip().split())

        return re.sub(r'[\W]+', '', _text, re.UNICODE)

    return ''


def precision_round(value, decimals, base=10):

    exp = math.pow(base, decimals)

    return round(value * exp) / exp


def generate_link(collection, feature_id, basepath=None):

    if basepath:

        return u'/%s/%s/%s' % (basepath, collection, feature_id)

    return u'/%s/%s' % (collection, feature_id)


def link_map(collection, feature_id):

    return {
        'data': generate_link(collection, feature_id, 'v1'),
        'html': generate_link(collection, feature_id)
    }


def convert_area(value, unit='acre'):

    unit_idx = {
        'acre': 0.0002471052,
        'hectare': 0.0001,
        'kilometer': 0.000001
    }

    if value and unit in unit_idx:

        return value * unit_idx.get(unit)

    return None


def truncate(text, length):

    #: Conditional will be falsey if
    #: text is None or empty string.

    if text and isinstance(text, basestring):

        return text[:length]

    return None


def parse_snake(text, operation=None):

    #: Conditional will be falsey if
    #: text is None or empty string.

    if text and isinstance(text, basestring):

        _tpl = text.replace('_', ' ')

        if operation == 'capitalize':

            _tpl.capitalize()

        elif operation == 'lower':

            _tpl.lower()

        elif operation == 'title':

            _tpl.title()

        elif operation == 'upper':

            _tpl.upper()

        return _tpl

    return None


def parse_query_limit(params, maximum=100):

    if isinstance(params, (dict, MultiDict, ImmutableMultiDict)):

        _limit = params.get('limit')

        if isinstance(_limit, int):

            return _limit

        if isinstance(_limit, basestring):

            try:

                return int(_limit)

            except (TypeError, ValueError) as error:

                pass

    return maximum


def parse_query_sort(cls, params):

    cols = cls.__table__.columns.keys()

    try:

        sort_tokens = params.get('sort').split(':')

        column = sort_tokens[0].lower().strip()

        if column in cols:

            direction = sort_tokens[1].lower().strip()

            if direction in ['ASC', 'DESC']:

                return '%s %s' % (column, direction)

            else:

                raise ValueError('Invalid direction parameter.')

        else:

            raise ValueError('Sort column not present.')

    except (AttributeError, IndexError, ValueError) as error:

        logger.debug(
            'app.utilities.parse_query_sort.error: %s',
            str(error))

        return 'id ASC'


def get_excluded_attrs(params):

    if isinstance(params, (dict, MultiDict, ImmutableMultiDict)):

        _excluded_attrs = params.get('exclude')

        if isinstance(_excluded_attrs, (list, tuple)):

            return _excluded_attrs

        elif isinstance(_excluded_attrs, basestring):

            return _excluded_attrs.split(',')

    return []


def shallow_collection(lst):

    _collection = [
        serializer.minimal_copy(feature)
        for feature in lst
    ]

    #: Maintain order of collection for equality comparisons.

    return sorted(_collection, key=lambda x: x.get('id'))


def extract_json_properties(obj, geom=True):

    properties = obj.get('properties')

    if isinstance(properties, dict):

        for key, value in properties.iteritems():

            if isinstance(value, dict):

                if 'id' in value:

                    obj[key] = value.get('properties')

                else:

                    obj[key] = value

            elif isinstance(value, list):

                obj[key] = [
                    relation.get('properties')
                    for relation in value
                ]

            else:

                obj[key] = value

        if not geom:

            obj.pop('geometry', None)
            
        obj.pop('properties', None)
        obj.pop('type', None)

    return obj


def scrub_request(model, data):

    logger.debug('utilities.scrub_request.data: %s', json.dumps(data)) 
    logger.debug('utilities.scrub_request.model: %s', model)
    logger.debug('utilities.scrub_request.dir(model): %s', dir(model))

    insp = inspect(model)

    whitelist = [
        attr for attr in insp.all_orm_descriptors.keys()
        if not(attr.startswith('_'))
    ]

    logger.debug('utilities.scrub_request.whitelist: %s', whitelist)

    inputs = data.keys()

    for attribute in inputs:

        if attribute not in whitelist:

            data.pop(attribute, None)

    return data


def validate_amount(data):

    amount = data.get('amount')

    logger.debug(
        'utilities.validate_amount.type(amount): %s',
        type(amount))

    if amount <= 10**12:

        if isinstance(amount, int):

            pass

        elif isinstance(amount, float):

            data['amount'] = precision_round(amount, 2)

        elif isinstance(amount, Decimal):

            pass

        else:

            data['amount'] = 0

    return data


def rgetattr(obj, attr, *args):
    """See https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects"""
    def _getattr(obj, attr):

        return getattr(obj, attr, *args)

    return reduce(_getattr, [obj] + attr.split('.'))
