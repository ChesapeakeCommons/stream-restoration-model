#!/usr/bin/env python

"""Define the BMPStormwater schema.

Created by Viable Industries, L.L.C. on 02/05/2017.
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


import math as Math


from datetime import datetime


from app import db
from app import logger


def reduction(inputs, value, load_data, preinstallation=False):

    """If the measurement_period is Pre-Installation the LER will use the
    raw installation_lateral_erosion_rate provided by the user.

    If the measurement_period is Planning or Installation the LER will be
    halved (i.e., multipled by 0.5).

    The Expert Panel (EP) guidance specifies a default value of 50%,
    subject to post-installation monitoring which could justify a larger
    reduction efficiency.[1]

    [1] Gene Yagow, Senior Research Scientist, Biological Systems
        Engineering Department Virginia Tech
    """
    return {
        'nitrogen': inputs.nitrogen(value, load_data, preinstallation=preinstallation),
        'phosphorus': inputs.phosphorus(value, load_data, preinstallation=preinstallation),
        'sediment': inputs.sediment(value, load_data, preinstallation=preinstallation)
    }


def installed_to_date(inputs, periods, percentage=False):

    planned_total_nitrogen = 0
    planned_total_phosphorus = 0
    planned_total_sediment = 0
    planned_gallons_per_year_of_stormwater_detained_or_infiltrated = 0
    planned_acres_of_protected_bmps_to_reduce_stormwater_runoff = 0
    planned_acres_of_installed_bmps_to_reduce_stormwater_runoff = 0
    planned_practice_1_extent = 0
    planned_practice_2_extent = 0
    planned_practice_3_extent = 0
    planned_practice_4_extent = 0
    planned_impervious_area = 0
    planned_total_drainage_area = 0

    installed_total_nitrogen = 0
    installed_total_phosphorus = 0
    installed_total_sediment = 0
    installed_gallons_per_year_of_stormwater_detained_or_infiltrated = 0
    installed_acres_of_protected_bmps_to_reduce_stormwater_runoff = 0
    installed_acres_of_installed_bmps_to_reduce_stormwater_runoff = 0
    installed_practice_1_extent = 0
    installed_practice_2_extent = 0
    installed_practice_3_extent = 0
    installed_practice_4_extent = 0
    installed_impervious_area = 0
    installed_total_drainage_area = 0

    for _index, _period in enumerate(periods):

        if _period.get('properties').get('measurement_period') == 'Planning':
            planned_total_nitrogen += _period.get('properties').get('planning').get('nitrogen', 0).get('value', 0)
            planned_total_phosphorus += _period.get('properties').get('planning').get('phosphorus', 0).get('value', 0)
            planned_total_sediment += _period.get('properties').get('planning').get('sediment', 0).get('value', 0)
            planned_gallons_per_year_of_stormwater_detained_or_infiltrated += _period.get('properties').get('metrics').get('gallons_per_year_of_stormwater_detained_or_infiltrated', 0)
            planned_acres_of_protected_bmps_to_reduce_stormwater_runoff += _period.get('properties').get('metrics').get('acres_of_protected_bmps_to_reduce_stormwater_runoff', 0)
            planned_acres_of_installed_bmps_to_reduce_stormwater_runoff += _period.get('properties').get('metrics').get('acres_of_installed_bmps_to_reduce_stormwater_runoff', 0)

            planned_practice_1_extent = _period.get('properties').get('practice_1_extent') if _period.get('properties').get('practice_1_extent') else 0
            planned_practice_2_extent = _period.get('properties').get('practice_2_extent') if _period.get('properties').get('practice_2_extent') else 0
            planned_practice_3_extent = _period.get('properties').get('practice_3_extent') if _period.get('properties').get('practice_3_extent') else 0
            planned_practice_4_extent = _period.get('properties').get('practice_4_extent') if _period.get('properties').get('practice_4_extent') else 0

            planned_impervious_area = _period.get('properties').get('impervious_area') if _period.get('properties').get('impervious_area') else 0
            planned_total_drainage_area = _period.get('properties').get('total_drainage_area') if _period.get('properties').get('total_drainage_area') else 0

        elif _period.get('properties').get('measurement_period') == 'Installation':
            installed_total_nitrogen += _period.get('properties').get('installation').get('nitrogen', 0).get('value', 0)
            installed_total_phosphorus += _period.get('properties').get('installation').get('phosphorus', 0).get('value', 0)
            installed_total_sediment += _period.get('properties').get('installation').get('sediment', 0).get('value', 0)
            installed_gallons_per_year_of_stormwater_detained_or_infiltrated += _period.get('properties').get('metrics').get('gallons_per_year_of_stormwater_detained_or_infiltrated', 0)
            installed_acres_of_protected_bmps_to_reduce_stormwater_runoff += _period.get('properties').get('metrics').get('acres_of_protected_bmps_to_reduce_stormwater_runoff', 0)
            installed_acres_of_installed_bmps_to_reduce_stormwater_runoff += _period.get('properties').get('metrics').get('acres_of_installed_bmps_to_reduce_stormwater_runoff', 0)

            installed_practice_1_extent = _period.get('properties').get('practice_1_extent') if _period.get('properties').get('practice_1_extent') else 0
            installed_practice_2_extent = _period.get('properties').get('practice_2_extent') if _period.get('properties').get('practice_2_extent') else 0
            installed_practice_3_extent = _period.get('properties').get('practice_3_extent') if _period.get('properties').get('practice_3_extent') else 0
            installed_practice_4_extent = _period.get('properties').get('practice_4_extent') if _period.get('properties').get('practice_4_extent') else 0
            installed_impervious_area = _period.get('properties').get('impervious_area') if _period.get('properties').get('impervious_area') else 0
            installed_total_drainage_area = _period.get('properties').get('total_drainage_area') if _period.get('properties').get('total_drainage_area') else 0

    _totals = {
        'nitrogen': installed_total_nitrogen,
        'phosphorus': installed_total_phosphorus,
        'sediment': installed_total_sediment,
        'gallons_per_year_of_stormwater_detained_or_infiltrated': installed_gallons_per_year_of_stormwater_detained_or_infiltrated,
        'acres_of_protected_bmps_to_reduce_stormwater_runoff': installed_acres_of_protected_bmps_to_reduce_stormwater_runoff,
        'acres_of_installed_bmps_to_reduce_stormwater_runoff': installed_acres_of_installed_bmps_to_reduce_stormwater_runoff,

        'practice_1_extent': installed_practice_1_extent,
        'practice_2_extent': installed_practice_2_extent,
        'practice_3_extent': installed_practice_3_extent,
        'practice_4_extent': installed_practice_4_extent,

        'impervious_area': installed_impervious_area,
        'total_drainage_area': installed_total_drainage_area,
    }

    if percentage:

        _totals = {
            'nitrogen': (installed_total_nitrogen/planned_total_nitrogen)*100 if planned_total_nitrogen > 0 else 0,
            'phosphorus': (installed_total_phosphorus/planned_total_phosphorus)*100 if planned_total_phosphorus > 0 else 0,
            'sediment': (installed_total_sediment/planned_total_sediment)*100 if planned_total_sediment > 0 else 0,

            'gallons_per_year_of_stormwater_detained_or_infiltrated': (installed_acres_of_protected_bmps_to_reduce_stormwater_runoff/planned_acres_of_protected_bmps_to_reduce_stormwater_runoff)*100 if planned_acres_of_protected_bmps_to_reduce_stormwater_runoff > 0 else 0,
            'acres_of_protected_bmps_to_reduce_stormwater_runoff': (installed_acres_of_protected_bmps_to_reduce_stormwater_runoff/planned_acres_of_protected_bmps_to_reduce_stormwater_runoff)*100 if planned_acres_of_protected_bmps_to_reduce_stormwater_runoff > 0 else 0,
            'acres_of_installed_bmps_to_reduce_stormwater_runoff': (installed_acres_of_installed_bmps_to_reduce_stormwater_runoff/planned_acres_of_installed_bmps_to_reduce_stormwater_runoff)*100 if planned_acres_of_installed_bmps_to_reduce_stormwater_runoff > 0 else 0,

            'practice_1_extent': (installed_practice_1_extent/planned_practice_1_extent)*100 if planned_practice_1_extent > 0 else 0,
            'practice_2_extent': (installed_practice_2_extent/planned_practice_2_extent)*100 if planned_practice_2_extent > 0 else 0,
            'practice_3_extent': (installed_practice_3_extent/planned_practice_3_extent)*100 if planned_practice_3_extent > 0 else 0,
            'practice_4_extent': (installed_practice_4_extent/planned_practice_4_extent)*100 if planned_practice_4_extent > 0 else 0,

            'impervious_area': (installed_impervious_area/planned_impervious_area)*100 if planned_impervious_area > 0 else 0,
            'total_drainage_area': (installed_total_drainage_area/planned_total_drainage_area)*100 if planned_total_drainage_area > 0 else 0,
        }

    return _totals


def adjustorCurveNitrogen(inputs, value):

    depthTreated = inputs.runoffDepthTreated(value)
    runoffVolumeCaptured = inputs.runoffVolumeCaptured(value)

    classification = value.get('site_reduction_classification', None)
    reduction = 0

    if classification == "Runoff Reduction":

        first = 0.0308*Math.pow(depthTreated, 5)
        second = 0.2562*Math.pow(depthTreated, 4)
        third = 0.8634*Math.pow(depthTreated, 3)
        fourth = 1.5285*Math.pow(depthTreated, 2)
        fifth = 1.501*depthTreated

        reduction = (first-second+third-fourth+fifth-0.013)

    elif classification == "Stormwater Treatment":

        first = 0.0152*Math.pow(depthTreated, 5)
        second = 0.131*Math.pow(depthTreated, 4)
        third = 0.4581*Math.pow(depthTreated, 3)
        fourth = 0.8418*Math.pow(depthTreated, 2)
        fifth = 0.8536*depthTreated

        reduction = (first-second+third-fourth+fifth-0.0046)

    return reduction


def adjustorCurvePhosphorus(inputs, value):

    depthTreated = inputs.runoffDepthTreated(value)
    runoffVolumeCaptured = inputs.runoffVolumeCaptured(value)

    classification = value.get('site_reduction_classification', None)
    reduction = 0

    if classification == "Runoff Reduction":

        first = 0.0304*Math.pow(depthTreated, 5)
        second = 0.2619*Math.pow(depthTreated, 4)
        third = 0.9161*Math.pow(depthTreated, 3)
        fourth = 1.6837*Math.pow(depthTreated, 2)
        fifth = 1.7072*depthTreated

        reduction = (first-second+third-fourth+fifth-0.0091)

    elif classification == "Stormwater Treatment":

        first = 0.0239*Math.pow(depthTreated, 5)
        second = 0.2058*Math.pow(depthTreated, 4)
        third = 0.7198*Math.pow(depthTreated, 3)
        fourth = 1.3229*Math.pow(depthTreated, 2)
        fifth = 1.3414*depthTreated

        reduction = (first-second+third-fourth+fifth-0.0072)

    return reduction


def adjustorCurveSediment(inputs, value):

    depthTreated = inputs.runoffDepthTreated(value)
    runoffVolumeCaptured = inputs.runoffVolumeCaptured(value)

    classification = value.get('site_reduction_classification', None)
    reduction = 0

    if classification == "Runoff Reduction":
        
        first = 0.0326*Math.pow(depthTreated, 5)
        second = 0.2806*Math.pow(depthTreated, 4)
        third = 0.9816*Math.pow(depthTreated, 3)
        fourth = 1.8039*Math.pow(depthTreated, 2)
        fifth = 1.8292*depthTreated

        reduction = (first-second+third-fourth+fifth-0.0098)

    elif classification == "Stormwater Treatment":

        first = 0.0304*Math.pow(depthTreated, 5)
        second = 0.2619*Math.pow(depthTreated, 4)
        third = 0.9161*Math.pow(depthTreated, 3)
        fourth = 1.6837*Math.pow(depthTreated, 2)
        fifth = 1.7072*depthTreated

        reduction = (first-second+third-fourth+fifth-0.0091)

    return reduction


def nitrogen(inputs, value, loaddata, preinstallation=False):

    multiplier = 1

    if preinstallation == False:

        multiplier = inputs.adjustorCurveNitrogen(value)

    impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0
    impervious_tn_ual = loaddata['impervious']['tn_ual'] if loaddata and 'impervious' in loaddata and 'tn_ual' in loaddata['impervious'] else 0
    total_drainage_area = value.get('total_drainage_area') if value.get('total_drainage_area') else 0

    return {
        "value": (((impervious_area * impervious_tn_ual) + ((total_drainage_area - impervious_area) * impervious_tn_ual)) * multiplier) / 43560,
        "adjustor": multiplier
    }


def phosphorus(inputs, value, loaddata, preinstallation=False):

    multiplier = 1

    if preinstallation == False:

        multiplier = inputs.adjustorCurvePhosphorus(value)

    impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0
    impervious_tp_ual = loaddata['impervious']['tp_ual'] if loaddata and 'impervious' in loaddata and 'tp_ual' in loaddata['impervious'] else 0
    total_drainage_area = value.get('total_drainage_area') if value.get('total_drainage_area') else 0

    return {
        "value": (((impervious_area * impervious_tp_ual) + ((total_drainage_area - impervious_area) * impervious_tp_ual)) * multiplier) / 43560,
        "adjustor": multiplier
    }


def sediment(inputs, value, loaddata, preinstallation=False):

    multiplier = 1

    if preinstallation == False:

        multiplier = inputs.adjustorCurveSediment(value)

    impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0
    impervious_tss_ual = loaddata['impervious']['tss_ual'] if loaddata and 'impervious' in loaddata and 'tss_ual' in loaddata['impervious'] else 0
    total_drainage_area = value.get('total_drainage_area') if value.get('total_drainage_area') else 0

    return {
        "value": (((impervious_area * impervious_tss_ual) + ((total_drainage_area - impervious_area) * impervious_tss_ual)) * multiplier) / 43560,
        "adjustor": multiplier
    }


def runoffDepthTreated(inputs, value):

    depthTreated = 1.0

    runoff_volume_captured = value.get('runoff_volume_captured') if value.get('runoff_volume_captured') else 0

    impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0

    if runoff_volume_captured and impervious_area:

      depthTreated = (runoff_volume_captured * 12) / (impervious_area / 43560)

    return depthTreated


def rainfallDepthTreated(inputs, value):

    depthTreated = inputs.runoffDepthTreated(value)

    impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0

    return (depthTreated/(impervious_area/43560)) * 12


def runoffVolumeCaptured(inputs, value):

    depthTreated = inputs.runoffDepthTreated(value)

    impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0

    return (depthTreated*impervious_area)/(12*43560)


def acres_of_protected_bmps_to_reduce_stormwater_runoff(inputs, value):

    total_drainage_area = value.get('total_drainage_area') if value.get('total_drainage_area') else 0

    return (total_drainage_area/43560)


def acres_of_installed_bmps_to_reduce_stormwater_runoff(inputs, value):

    practice_1_extent = value.get('practice_1_extent') if value.get('practice_1_extent') else 0
    practice_2_extent = value.get('practice_2_extent') if value.get('practice_2_extent') else 0
    practice_3_extent = value.get('practice_3_extent') if value.get('practice_3_extent') else 0
    practice_4_extent = value.get('practice_4_extent') if value.get('practice_4_extent') else 0

    return practice_1_extent+practice_2_extent+practice_3_extent+practice_4_extent;


def gallons_per_year_of_stormwater_detained_or_infiltrated(inputs, value):

    gallons_ = 0

    runoff_volume_captured = value.get('runoff_volume_captured') if value.get('runoff_volume_captured') else 0

    if runoff_volume_captured:

      gallons_ = (runoff_volume_captured * 325851.4)

    return gallons_
