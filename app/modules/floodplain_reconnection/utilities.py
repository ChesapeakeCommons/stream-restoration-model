#!/usr/bin/env python

'''Define the EnhancedStreamRestoration schema.

Created by Viable Industries, L.L.C. on 02/05/2015.
Copyright 2016 Viable Industries, L.L.C. All rights reserved.

For license and copyright information please see the LICENSE document (the
'License') included with this software package. This file may not be used
in any manner except in compliance with the License unless required by
applicable law or agreed to in writing, software distributed under the
License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
'''

# Import standard dependencies

import math as Math
from datetime import datetime

# Import package dependencies

from app import logger

# Import module dependencies

from .constants import URBAN_STATE_UAL as load_data


def efficiency(key):
    
    idx = {
        'n_eff': 0.2,
        'p_eff': 0.3,
        's_eff': 0.2
    }

    return idx.get(key, 0)


def reduction(data):

    '''If the measurement_period is Pre-Installation the LER will use the
    raw installation_lateral_erosion_rate provided by the user.

    If the measurement_period is Planning or Installation the LER will be
    halved (i.e., multipled by 0.5).

    The Expert Panel (EP) guidance specifies a default value of 50%,
    subject to post-installation monitoring which could justify a larger
    reduction efficiency.[1]

    [1] Gene Yagow, Senior Research Scientist, Biological Systems
        Engineering Department Virginia Tech
    '''
    if data.get('has_majority_design_completion', False):

        # return {
        #     'tn_lbs_reduced': nitrogen_protocol_3(data),
        #     'tp_lbs_reduced': phosphorus_protocol_3(data),
        #     'tss_tons_reduced': sediment_protocol_1(data)
        # }

        return {
            'tn_lbs_reduced': data.get('tn_lbs_reduced', 0),
            'tp_lbs_reduced': data.get('tp_lbs_reduced', 0),
            'tss_tons_reduced': data.get('tss_tons_reduced', 0)
        }

    else:

        return {
            'tn_lbs_reduced': nitrogen(data),
            'tp_lbs_reduced': phosphorus(data),
            'tss_tons_reduced': sediment(data)
        }


def bank_height_ratio(bank_height, bankfull_height):

    behi = 0

    if bank_height:

        behi = (bank_height / bankfull_height)

    return behi


def nitrogen_protocol_2(data):

    project_left_bank_height = data.get('project_left_bank_height', 0)
    left_bank_bankfull_height = data.get('left_bank_bankfull_height', 0)

    project_right_bank_height = data.get('project_right_bank_height', 0)
    right_bank_bankfull_height = data.get('right_bank_bankfull_height', 0)

    bulk_density = 125
    nitrogen = 0
    left_behi = bank_height_ratio(project_left_bank_height, left_bank_bankfull_height)
    right_behi = bank_height_ratio(project_right_bank_height, right_bank_bankfull_height)
    left_bank = 0
    right_bank = 0
    year = 365
    coefficient = 0.000195

    '''NOVEMBER 2017 MDNR UPDATES

    1. CHANGE CO-EFFICIENT FROM 0.000195 to 0.075
    2. Change the BEHI+

    '''

    length_of_left_bank_with_improved_connectivity = data.get('length_of_left_bank_with_improved_connectivity', 0)
    length_of_right_bank_with_improved_connectivity = data.get('length_of_right_bank_with_improved_connectivity', 0)
    stream_width_at_mean_base_flow = data.get('stream_width_at_mean_base_flow', 0)

    if left_behi < 1.1:

        left_bank = length_of_left_bank_with_improved_connectivity * (stream_width_at_mean_base_flow / 2 + 5)

    if right_behi < 1.1:

        right_bank = length_of_right_bank_with_improved_connectivity * (stream_width_at_mean_base_flow / 2 + 5)

    nitrogen = ((left_bank + right_bank) * 5 * bulk_density / 2000) * coefficient * year

    return nitrogen


def nitrogen_protocol_3(data):

    _eff = efficiency('n_eff')

    watershed_impervious_area = data.get('watershed_impervious_area', 0)
        
    return _eff * (watershed_impervious_area * load_data['impervious']['tn_ual'] + watershed_impervious_area * load_data['pervious']['tn_ual'])


def phosphorus_protocol_3(data):

    _eff = efficiency('p_eff')

    watershed_impervious_area = data.get('watershed_impervious_area', 0)
        
    return _eff * (watershed_impervious_area * load_data['impervious']['tp_ual'] + watershed_impervious_area * load_data['pervious']['tp_ual'])


def sediment_protocol_1(data):

    _eff = efficiency('s_eff')

    watershed_impervious_area = data.get('watershed_impervious_area', 0)
        
    return _eff * (watershed_impervious_area * load_data['impervious']['tss_ual'] + watershed_impervious_area * load_data['pervious']['tss_ual'])


def nitrogen(data):

    coastal_ = 0
    noncoastal_ = 0

    if data.get('override_linear_feet_in_coastal_plain', 0):

        coastal_ = data.get('override_linear_feet_in_coastal_plain', 0) * 0.075

    if data.get('override_linear_feet_in_noncoastal_plain', 0):

        noncoastal_ = data.get('override_linear_feet_in_noncoastal_plain', 0) * 0.075

    return (coastal_ + noncoastal_)


def phosphorus(data):

    coastal_ = 0
    noncoastal_ = 0

    if data.get('override_linear_feet_in_coastal_plain', 0):

        coastal_ = data.get('override_linear_feet_in_coastal_plain', 0) * 0.068

    if data.get('override_linear_feet_in_noncoastal_plain', 0):

        noncoastal_ = data.get('override_linear_feet_in_noncoastal_plain', 0) * 0.068

    return (coastal_ + noncoastal_)


def sediment(data):

    coastal_ = 0
    noncoastal_ = 0

    if data.get('override_linear_feet_in_coastal_plain'):

        coastal_ = data.get('override_linear_feet_in_coastal_plain') * 15.13

    if data.get('override_linear_feet_in_noncoastal_plain'):

        noncoastal_ = data.get('override_linear_feet_in_noncoastal_plain') * 44.88

    return ((coastal_ + noncoastal_) / 2000)


def miles_of_streambank_restored(data):

    miles = 0

    if not data.get('has_majority_design_completion'):

        coastal_ = 0
        noncoastal_ = 0

        if data.get('override_linear_feet_in_coastal_plain', 0):

            coastal_ = data.get('override_linear_feet_in_coastal_plain', 0)

        if data.get('override_linear_feet_in_noncoastal_plain', 0):

            noncoastal_ = data.get('override_linear_feet_in_noncoastal_plain', 0)

        miles = ((coastal_ + noncoastal_) / 5280)

        return miles

    project_left_bank_height = data.get('project_left_bank_height', 0)
    left_bank_bankfull_height = data.get('left_bank_bankfull_height', 0)

    project_right_bank_height = data.get('project_right_bank_height', 0)
    right_bank_bankfull_height = data.get('right_bank_bankfull_height', 0)

    length_of_left_bank_with_improved_connectivity = data.get('length_of_left_bank_with_improved_connectivity', 0)
    length_of_right_bank_with_improved_connectivity = data.get('length_of_right_bank_with_improved_connectivity', 0)

    stream_width_at_mean_base_flow = data.get('stream_width_at_mean_base_flow', 0)
    stream_length_reconnected_at_floodplain = data.get('stream_length_reconnected_at_floodplain', 0)

    left_behi = bank_height_ratio(project_left_bank_height, left_bank_bankfull_height)
    right_behi = bank_height_ratio(project_right_bank_height, right_bank_bankfull_height)
    left_bank = 0
    right_bank = 0
    feet_to_miles = 5280

    if left_behi < 1.1:

        left_bank = length_of_left_bank_with_improved_connectivity

    if right_behi < 1.1:

        right_bank = length_of_right_bank_with_improved_connectivity

    miles = ((left_bank + right_bank + stream_length_reconnected_at_floodplain) / feet_to_miles)

    return miles


def acres_of_streambank_restored(data):

    project_left_bank_height = data.get('project_left_bank_height', 0)
    left_bank_bankfull_height = data.get('left_bank_bankfull_height', 0)

    project_right_bank_height = data.get('project_right_bank_height', 0)
    right_bank_bankfull_height = data.get('right_bank_bankfull_height', 0)

    length_of_left_bank_with_improved_connectivity = data.get('length_of_left_bank_with_improved_connectivity', 0)
    length_of_right_bank_with_improved_connectivity = data.get('length_of_right_bank_with_improved_connectivity', 0)

    stream_width_at_mean_base_flow = data.get('stream_width_at_mean_base_flow', 0)
    stream_length_reconnected_at_floodplain = data.get('stream_length_reconnected_at_floodplain', 0)

    acres = 0
    left_behi = bank_height_ratio(project_left_bank_height, left_bank_bankfull_height)
    right_behi = bank_height_ratio(project_right_bank_height, right_bank_bankfull_height)
    left_bank = 0
    right_bank = 0
    to_acres = 43560

    if left_behi < 1.1:

        left_bank = length_of_left_bank_with_improved_connectivity

    if right_behi < 1.1:

        right_bank = length_of_right_bank_with_improved_connectivity

    acres = (((left_bank * (stream_width_at_mean_base_flow / 2 + 5)) + (right_bank * (stream_width_at_mean_base_flow / 2 + 5)) + stream_length_reconnected_at_floodplain) / to_acres)

    return acres


def acres_of_floodplain_reconnected(data):

    acres = data.get('connected_floodplain_surface_area', 0)

    return acres
