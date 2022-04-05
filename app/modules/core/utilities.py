#!/usr/bin/env python

from flask import abort
from flask import request

from app import logger
from app.modules import bank_stabilization
from app.modules import default
from app.modules import denitrification
from app.modules import floodplain_reconnection_1
from app.modules import floodplain_reconnection_2
from app.modules import floodplain_reconnection_3
from app.modules import instream_habitat
from app.modules import instream_processing
from app.modules import outfall_and_gully_stabilization
from app.modules import outfall_stabilization
from app.modules import prevented_sediment
from app.modules import shoreline_management
from app.modules import stormwater
from app.modules import swp
from app.utilities import rgetattr


def validate_request(data):

    try:

        practice_code = data.get('practice_code')

        return practice_code and isinstance(practice_code, str)

    except (AttributeError, KeyError):

        return False


def get_mod_name(string):

    return string.rsplit('.', 1)[1]


def handle_request(data):

    logger.debug(
        'core.utilities.handle_request: %s',
        str(request))

    func_idx = {
        get_mod_name(module.__name__): rgetattr(module, 'utilities')
        for module in [
            bank_stabilization,
            default,
            denitrification,
            floodplain_reconnection_1,
            floodplain_reconnection_2,
            floodplain_reconnection_3,
            instream_habitat,
            instream_processing,
            outfall_stabilization,
            outfall_and_gully_stabilization,
            prevented_sediment,
            shoreline_management,
            stormwater,
            swp,
        ]
    }

    logger.debug(
        'core.utilities.handle_request.func_idx: %s',
        func_idx)

    if validate_request(data):

        codes = data.get('practice_code', '').split('.')

        if codes[0] in func_idx:

            if len(codes) > 1:

                data.update({
                    'secondary_code': codes[1]
                })

            return func_idx.get(codes[0]).reduction(data)

        else:

            abort(400, 'Invalid `practice_code` parameter.')

    else:

        abort(400, 'Empty or invalid request body.')


def fetch_tpl_path(practice_type):

    logger.debug(
        'core.utilities.fetch_tpl: %s',
        practice_type)

    tpl_idx = {
        practice: '%s.html' % practice.replace('_', '-')
        for practice in [
            'bank_stabilization',
            'floodplain_reconnection',
            'instream_habitat',
            'instream_processing',
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
