#!/usr/bin/env python

from __future__ import division

from app import logger
from app.utilities import product


def base_tn(value):

    return value * 0.00269


def final_tn(operands, value):
    operands.append(value)
    return product(operands)


def tn_reduction(data):

    floodplain_sq_ft = data.get('floodplain_sq_ft', 0)

    channel_sq_ft = data.get('channel_sq_ft', 0)

    # Baseflow reduction factor

    brf = data.get('brf', 0)

    # Floodplain height factor

    fhf = data.get('fhf', 0)

    # Aquifer conductivity reduction factor

    acrf = data.get('acrf', 0)

    values = [
        floodplain_sq_ft,
        channel_sq_ft,
        brf,
        fhf,
        acrf,
    ]

    if not all(isinstance(x, (float, int)) for x in values):

        return 0

    floodplain_tn = base_tn(floodplain_sq_ft)

    channel_tn = base_tn(channel_sq_ft)

    discount_factors = [brf, fhf, acrf]

    total_floodplain_tn = final_tn(discount_factors, floodplain_tn)

    total_channel_tn = final_tn(discount_factors, channel_tn)

    # See: https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2021/07/P2-DESIGN-EXAMPLE.pdf

    try:

        return total_floodplain_tn + total_channel_tn

    except (ValueError, ZeroDivisionError):

        return 0


def phased_reduction(data):

    pre = data.get('pre', {})

    post = data.get('post', {})

    pre_tn = tn_reduction(pre)

    post_tn = tn_reduction(post)

    return {
        'tn_lbs_reduced': post_tn - pre_tn
    }


def reduction(data):
    if 'pre' in data and 'post' in data:
        return phased_reduction(data)

    floodplain_sq_ft = data.get('floodplain_sq_ft', 0)

    channel_sq_ft = data.get('channel_sq_ft', 0)

    # Baseflow reduction factor

    brf = data.get('brf', 0)

    # Floodplain height factor

    fhf = data.get('fhf', 0)

    # Aquifer conductivity reduction factor

    acrf = data.get('acrf', 0)

    values = [
        floodplain_sq_ft,
        channel_sq_ft,
        brf,
        fhf,
        acrf,
    ]

    res = {
        'tn_lbs_reduced': 0
    }

    if not all(isinstance(x, (float, int)) for x in values):
        return res

    floodplain_tn = base_tn(floodplain_sq_ft)

    logger.warning(
        'denitrification.utilities.reduction:floodplain_tn: %s',
        floodplain_tn
    )

    channel_tn = base_tn(channel_sq_ft)

    logger.warning(
        'denitrification.utilities.reduction:channel_tn: %s',
        channel_tn
    )

    discount_factors = [brf, fhf, acrf]

    logger.warning(
        'denitrification.utilities.reduction:floodplain_tn: %s',
        discount_factors
    )

    total_floodplain_tn = final_tn(discount_factors, floodplain_tn)

    logger.warning(
        'denitrification.utilities.reduction:total_floodplain_tn: %s',
        total_floodplain_tn
    )

    total_channel_tn = final_tn(discount_factors, channel_tn)

    logger.warning(
        'denitrification.utilities.reduction:total_channel_tn: %s',
        total_channel_tn
    )

    # See: https://chesapeakestormwater.net/wp-content/uploads/dlm_uploads/2021/07/P2-DESIGN-EXAMPLE.pdf

    try:

        total = total_floodplain_tn + total_channel_tn

        return {
            'tn_lbs_reduced': total
        }

    except (ValueError, ZeroDivisionError):

        return res
