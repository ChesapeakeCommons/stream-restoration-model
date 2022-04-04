#!/usr/bin/env python

import math as Math

from app import logger
from .constants import URBAN_STATE_UAL as load_data


def reduction(data, preinstallation=False):

    """If the measurement_period is Pre-Installation the LER will use the
    raw installation_lateral_erosion_rate provided by the user.

    If the measurement_period is Planning or Installation the LER will be
    halved (i.e., multipled by 0.5).

    The Expert Panel (EP) guidance specifies a default data of 50%,
    subject to post-installation monitoring which could justify a larger
    reduction efficiency.[1]

    [1] Gene Yagow, Senior Research Scientist, Biological Systems
        Engineering Department Virginia Tech
    """

    n_result = nitrogen(data)
    p_result = phosphorus(data)
    tss_result = sediment(data)

    return {
        'tn_lbs_reduced': n_result.get('reduction'),
        'tn_lbs_reduced': p_result.get('reduction'),
        'tss_tons_reduced': tss_result.get('reduction'),
        'n_curve': tss_result.get('curve'),
        'p_curve': tss_result.get('curve'),
        'tss_curve': tss_result.get('curve')
    }


def adjustor_curve_nitrogen(data):

    depth_treated = runoff_depth_treated(data)

    # runoff_volume_captured = runoff_volume_captured(data)

    reduction = 0.0

    first = 0.0308 * Math.pow(depth_treated, 5)

    second = 0.2562 * Math.pow(depth_treated, 4)

    third = 0.8634 * Math.pow(depth_treated, 3)

    fourth = 1.5285 * Math.pow(depth_treated, 2)

    fifth = 1.501 * depth_treated

    reduction = (first - second + third - fourth + fifth - 0.013)

    return reduction


def adjustor_curve_phosphorus(data):

    depth_treated = runoff_depth_treated(data)

    # runoff_volume_captured = runoff_volume_captured(data)

    reduction = 0.0

    first = 0.0304 * Math.pow(depth_treated, 5)
    second = 0.2619 * Math.pow(depth_treated, 4)
    third = 0.9161 * Math.pow(depth_treated, 3)
    fourth = 1.6837 * Math.pow(depth_treated, 2)
    fifth = 1.7072 * depth_treated

    reduction = (first - second + third - fourth + fifth - 0.0091)

    return reduction


def adjustor_curve_sediment(data):

    depth_treated = runoff_depth_treated(data)

    # runoff_volume_captured = runoff_volume_captured(data)

    reduction = 0.0
        
    first = 0.0326 * Math.pow(depth_treated, 5)
    second = 0.2806 * Math.pow(depth_treated, 4)
    third = 0.9816 * Math.pow(depth_treated, 3)
    fourth = 1.8039 * Math.pow(depth_treated, 2)
    fifth = 1.8292 * depth_treated

    reduction = (first - second + third - fourth + fifth - 0.0098)

    return reduction


def nitrogen(data, preinstallation=False):

    multiplier = 1.0

    if preinstallation == False:

        multiplier = adjustor_curve_nitrogen(data)

    impervious_area = data.get('impervious_area', 0)
    impervious_tn_ual = load_data['impervious']['tn_ual']
    total_drainage_area = data.get('total_drainage_area', 0)

    return {
        "reduction": (((impervious_area * impervious_tn_ual) + ((total_drainage_area - impervious_area) * impervious_tn_ual)) * multiplier) / 43560,
        "curve": multiplier
    }


def phosphorus(data, preinstallation=False):

    multiplier = 1.0

    if preinstallation == False:

        multiplier = adjustor_curve_phosphorus(data)

    impervious_area = data.get('impervious_area', 0)
    impervious_tp_ual = load_data['impervious']['tp_ual']
    total_drainage_area = data.get('total_drainage_area', 0)

    return {
        "reduction": (((impervious_area * impervious_tp_ual) + ((total_drainage_area - impervious_area) * impervious_tp_ual)) * multiplier) / 43560,
        "curve": multiplier
    }


def sediment(data, preinstallation=False):

    multiplier = 1.0

    if preinstallation == False:

        multiplier = adjustor_curve_sediment(data)

    impervious_area = data.get('impervious_area', 0)
    impervious_tss_ual = load_data['impervious']['tss_ual']
    total_drainage_area = data.get('total_drainage_area', 0)

    return {
        "reduction": (((impervious_area * impervious_tss_ual) + ((total_drainage_area - impervious_area) * impervious_tss_ual)) * multiplier) / 43560,
        "curve": multiplier
    }


def runoff_depth_treated(data):

    logger.debug(
        'stormwater.utilities.runoff_depth_treated.data: %s',
        data)

    depth_treated = 1.0

    runoff_volume_captured = float(data.get('runoff_volume_captured', 0))

    logger.debug(
        'stormwater.utilities.runoff_depth_treated.runoff_volume_captured: %s',
        runoff_volume_captured)

    impervious_area = float(data.get('impervious_area', 0))

    logger.debug(
        'stormwater.utilities.runoff_depth_treated.impervious_area: %s',
        impervious_area)

    if runoff_volume_captured and impervious_area:

      depth_treated = (runoff_volume_captured * 12) / (impervious_area / 43560)

    return depth_treated


def rainfall_depth_treated(data):

    depth_treated = runoff_depth_treated(data)

    impervious_area = float(data.get('impervious_area', 0))

    return (depth_treated / (impervious_area / 43560)) * 12


def runoff_volume_captured(data):

    depth_treated = runoff_depth_treated(data)

    impervious_area = float(data.get('impervious_area', 0))

    return (depth_treated * impervious_area) / (float(12) * 43560)


def acres_of_protected_bmps_to_reduce_stormwater_runoff(data):

    total_drainage_area = float(data.get('total_drainage_area', 0))

    return (total_drainage_area / 43560)


def acres_of_installed_bmps_to_reduce_stormwater_runoff(data):

    return data.get('practice_extent', 0)


def gallons_per_year_of_stormwater_detained_or_infiltrated(data):

    gallons_ = 0

    runoff_volume_captured = float(data.get('runoff_volume_captured', 0))

    if runoff_volume_captured:

      gallons_ = (runoff_volume_captured * 325851.4)

    return gallons_
