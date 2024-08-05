#!/usr/bin/env python

from __future__ import division

from app import logger
from app.utilities import numeric_fallback
from app.utilities import product


def base_tn(value):

    return value * 0.00269


def zone_reduction(
    data,
    area,
    zone,
    phase,
):

    # Baseflow reduction factor

    brf = numeric_fallback(
        data.get(zone).get('brf'),
        fallback=0,
    )

    # Floodplain height factor

    fhf = numeric_fallback(
        data.get(zone).get('fhf'),
        fallback=0,
    )

    # Aquifer conductivity reduction factor

    acrf = numeric_fallback(
        data.get(zone).get('acrf'),
        fallback=0,
    )

    values = [
        area,
        brf,
        fhf,
        acrf,
    ]

    if not all(isinstance(x, (float, int)) for x in values):
        return 0

    zone_tn = base_tn(area)

    logger.warning(
        'denitrification.utilities.zone_reduction.'
        'zone_tn: %s [%s]',
        zone_tn,
        phase,
    )

    discount_factors = [brf, fhf, acrf]

    logger.warning(
        'denitrification.utilities.zone_reduction.'
        'discount_factors: %s [%s]',
        discount_factors,
        phase,
    )

    total_zone_tn = product([
        brf,
        fhf,
        acrf,
        zone_tn,
    ])

    logger.warning(
        'denitrification.utilities.zone_reduction.'
        'total_zone_tn: %s [%s]',
        total_zone_tn,
        phase,
    )

    return total_zone_tn


def tn_reduction(data, phase='default'):

    floodplain_sq_ft = numeric_fallback(
        data.get('floodplain_sq_ft'),
        fallback=0,
    )

    channel_sq_ft = numeric_fallback(
        data.get('channel_sq_ft'),
        fallback=0,
    )

    try:
        total_floodplain_tn = zone_reduction(
            data=data,
            area=floodplain_sq_ft,
            zone='floodplain',
            phase=phase,
        )
    except (ValueError, ZeroDivisionError):
        total_floodplain_tn = 0.0

    try:
        total_channel_tn = zone_reduction(
            data=data,
            area=channel_sq_ft,
            zone='channel',
            phase=phase,
        )
    except (ValueError, ZeroDivisionError):
        total_channel_tn = 0.0

    return total_floodplain_tn + total_channel_tn

    # # Baseflow reduction factor
    #
    # brf = numeric_fallback(
    #     data.get('brf'),
    #     fallback=0,
    # )
    #
    # # Floodplain height factor
    #
    # fhf = numeric_fallback(
    #     data.get('fhf'),
    #     fallback=0,
    # )
    #
    # # Aquifer conductivity reduction factor
    #
    # acrf = numeric_fallback(
    #     data.get('acrf'),
    #     fallback=0,
    # )
    #
    # values = [
    #     floodplain_sq_ft,
    #     channel_sq_ft,
    #     brf,
    #     fhf,
    #     acrf,
    # ]
    #
    # if not all(isinstance(x, (float, int)) for x in values):
    #     return 0
    #
    # floodplain_tn = base_tn(floodplain_sq_ft)
    #
    # logger.warning(
    #     'denitrification.utilities.tn_reduction.'
    #     'floodplain_tn: %s [%s]',
    #     floodplain_tn,
    #     phase,
    # )
    #
    # channel_tn = base_tn(channel_sq_ft)
    #
    # logger.warning(
    #     'denitrification.utilities.tn_reduction.'
    #     'channel_tn: %s [%s]',
    #     channel_tn,
    #     phase,
    # )
    #
    # discount_factors = [brf, fhf, acrf]
    #
    # logger.warning(
    #     'denitrification.utilities.tn_reduction.'
    #     'discount_factors: %s [%s]',
    #     discount_factors,
    #     phase,
    # )
    #
    # total_floodplain_tn = product([
    #     brf,
    #     fhf,
    #     acrf,
    #     floodplain_tn,
    # ])
    #
    # logger.warning(
    #     'denitrification.utilities.tn_reduction.'
    #     'total_floodplain_tn: %s [%s]',
    #     total_floodplain_tn,
    #     phase,
    # )
    #
    # total_channel_tn = product([
    #     brf,
    #     fhf,
    #     acrf,
    #     channel_tn,
    # ])
    #
    # logger.warning(
    #     'denitrification.utilities.tn_reduction.'
    #     'total_channel_tn: %s [%s]',
    #     total_channel_tn,
    #     phase,
    # )
    #
    # # See: https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2021/07/P2-DESIGN-EXAMPLE.pdf
    #
    # try:
    #
    #     return total_floodplain_tn + total_channel_tn
    #
    # except (ValueError, ZeroDivisionError):
    #
    #     return 0


def phased_reduction(data):

    pre = data.get('pre', {})

    post = data.get('post', {})

    pre_tn = tn_reduction(pre, phase='pre')

    logger.warning(
        'denitrification.utilities.phased_reduction.'
        'pre_tn: %s',
        pre_tn
    )

    post_tn = tn_reduction(post, phase='post')

    logger.warning(
        'denitrification.utilities.phased_reduction.'
        'post_tn: %s',
        post_tn
    )

    return {
        'tn_lbs_reduced': post_tn - pre_tn
    }


def reduction(data):
    if 'pre' in data and 'post' in data:
        return phased_reduction(data)

    return {
        'tn_lbs_reduced': tn_reduction(data)
    }
