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

from datetime import datetime
from decimal import Decimal

# Import Flask dependencies

from flask import abort
from flask import json
from flask import request

# Import package dependencies

from app import db
from app import logger
from app import serializer

from app.modules import bank_stabilization
from app.modules import enhanced_stream_restoration
from app.modules import instream_habitat
from app.modules import stormwater

from app.schema.practice import Practice

from app.utilities import extract_json_properties
from app.utilities import geom_as_wkt
from app.utilities import parse_geometry
from app.utilities import truncate
from app.utilities import scrub_request


def calculate_reduction(obj, value, attr):

    if isinstance(value, (int, float)):

        multiplier = getattr(obj, attr)

        return round((Decimal(value) * multiplier), 4)

    return 0


def validate_request(data):

    try:

        practice_code = data.get('practice_code')

        unit_quantity = data.get('units')

        return (practice_code and unit_quantity and
                isinstance(practice_code, basestring) and
                isinstance(unit_quantity, (float, int)))

    except (AttributeError, KeyError):

        return False


def handle_request(data):

    logger.debug(
        'core.utilities.handle_request: %s',
        str(request))

    func_idx = {
        module.__name__: getattr(module, 'reduction')
        for module in [
            bank_stabilization,
            enhanced_stream_restoration,
            instream_habitat,
            stormwater
        ]
    }

    if validate_request(data):

        practice_type = data.get('practice_code')

        if practice_type in func_idx:

            return func_idx.get(practice_type)(data)

        else:

            abort(400, 'Invalid `practice_code` parameter.')

    else:

        abort(400, 'Empty or invalid request body.')


def fetch_tpl_path(practice_type):

    logger.debug(
        'core.utilities.fetch_tpl: %s',
        practice_type)

    tpl_idx = {
        practice: '%s.html' % practice
        for practice in [
            'bank_stabilization',
            'enhanced_stream_restoration',
            'instream_habitat',
            'stormwater'
        ]
    }

    logger.debug(
        'core.utilities.tpl_idx: %s',
        tpl_idx)

    practice_type = practice_type.replace('-', '_')

    logger.debug(
        'core.utilities.stripped_type: %s',
        practice_type)

    if practice_type in tpl_idx:

        return tpl_idx.get(practice_type)

    else:

        abort(400, 'Invalid `practice_code` parameter.')
