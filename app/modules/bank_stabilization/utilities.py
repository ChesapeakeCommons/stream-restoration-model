#!/usr/bin/env python

"""Define the BMPBankStabilization schema.

Created by Viable Industries, L.L.C. on 02/05/2015.
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


import math


from datetime import datetime


from app import db
from app import logger


def reduction(inputs, value, preinstallation=False):

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
    installation_lateral_erosion_rate = value.get('installation_lateral_erosion_rate', 0) if value.get('installation_lateral_erosion_rate', 0) else 0
    installation_length_of_streambank = value.get('installation_length_of_streambank', 0) if value.get('installation_length_of_streambank', 0) else 0
    installation_soil_bulk_density = value.get('installation_soil_bulk_density', 0) if value.get('installation_soil_bulk_density', 0) else 0

    ler = installation_lateral_erosion_rate * 0.5

    if preinstallation:
        ler = installation_lateral_erosion_rate

    base_length = installation_length_of_streambank
    soil_density = installation_soil_bulk_density

    installation_eroding_bank_height = value.get('installation_eroding_bank_height', 0) if value.get('installation_eroding_bank_height', 0) else 0
    installation_eroding_bank_horizontal_width = value.get('installation_eroding_bank_horizontal_width', 0) if value.get('installation_eroding_bank_horizontal_width', 0) else 0

    square_root = math.sqrt((installation_eroding_bank_height * installation_eroding_bank_height) + (installation_eroding_bank_horizontal_width * installation_eroding_bank_horizontal_width))
    load_total = base_length * square_root * ler * soil_density

    installation_soil_n_content = value.get('installation_soil_n_content', 0) if value.get('installation_soil_n_content', 0) else 0
    installation_soil_p_content = value.get('installation_soil_p_content', 0) if value.get('installation_soil_p_content', 0) else 0

    return {
        'nitrogen': ((load_total)/2000)*installation_soil_n_content,
        'phosphorus': ((load_total)/2000)*installation_soil_p_content,
        'sediment': (load_total)/2000
    }


def miles_of_streambank_restored(inputs, value):

    installation_length_of_streambank = value.get('installation_length_of_streambank', 0) if value.get('installation_length_of_streambank', 0) else 0

    return (installation_length_of_streambank / 5280)
