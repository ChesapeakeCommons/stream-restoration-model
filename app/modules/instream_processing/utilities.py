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

        return {
            'tn_lbs_reduced': nitrogen_protocol_2(data)
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

    hyporheic_box_depth = data.get('hyporheic_box_depth', 0)

    if hyporheic_box_depth > 5:

        hyporheic_box_depth = 5

    bulk_density = data.get('bulk_density_of_soil_in_hyporheic_zone ', 125)

    nitrogen = 0
    left_behi = bank_height_ratio(project_left_bank_height, left_bank_bankfull_height)
    right_behi = bank_height_ratio(project_right_bank_height, right_bank_bankfull_height)
    left_bank = 0
    right_bank = 0
    days_per_year = 365
    coefficient = 0.000195

    '''NOVEMBER 2017 MDNR UPDATES

    1. CHANGE CO-EFFICIENT FROM 0.000195 to 0.075
    2. Change the BEHI+

    '''

    # '=stream length * (stream width + 10) * 5 * bulk density / 2000 lbs/ton * 0.000195 lbs/ton/day * 365 days/yr

    # '=stream length * (stream width + 10) * hyporheic box ft depth * bulk density / 2000 lbs/ton * 0.000195 lbs/ton/day * 365 days/yr

    length_of_left_bank_with_improved_connectivity = data.get('length_of_left_bank_with_improved_connectivity', 0)
    length_of_right_bank_with_improved_connectivity = data.get('length_of_right_bank_with_improved_connectivity', 0)
    stream_width_at_mean_base_flow = data.get('stream_width_at_mean_base_flow', 0)

    if left_behi < 1.1:

        left_bank = length_of_left_bank_with_improved_connectivity * (stream_width_at_mean_base_flow / 2 + 5)

    if right_behi < 1.1:

        right_bank = length_of_right_bank_with_improved_connectivity * (stream_width_at_mean_base_flow / 2 + 5)

    nitrogen = ((left_bank + right_bank) * hyporheic_box_depth * bulk_density / 2000) * coefficient * days_per_year

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

    reduction_ = 0

    linear_feet = data.get('linear_feet')

    if isinstance(linear_feet, (float, int)):

        reduction_ = linear_feet * 0.075

    return reduction_


def phosphorus(data):

    reduction_ = 0

    linear_feet = data.get('linear_feet')

    if isinstance(linear_feet, (float, int)):

        reduction_ = linear_feet * 0.068

    return reduction_


def sediment(data):

    reduction_ = 0

    linear_feet = data.get('linear_feet')

    if isinstance(linear_feet, (float, int)):

        reduction_ = linear_feet * 248.0

    return reduction_
