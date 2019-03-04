#!/usr/bin/env python

"""Define the BankStabilization schema.

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

# Import standard dependencies

import math
from datetime import datetime

# Import package dependencies

from app import logger


def reduction(data):

    """If the measurement_period is Pre-Installation the LER will use the
    raw lateral_erosion_rate provided by the user.

    If the measurement_period is Planning or Installation the LER will be
    halved (i.e., multipled by 0.5).

    The Expert Panel (EP) guidance specifies a default value of 50%,
    subject to post-installation monitoring which could justify a larger
    reduction efficiency.[1]

    [1] Gene Yagow, Senior Research Scientist, Biological Systems
        Engineering Department Virginia Tech
    """
    lateral_erosion_rate = data.get('lateral_erosion_rate', 0) if data.get('lateral_erosion_rate', 0) else 0
    length_of_streambank = data.get('length_of_streambank', 0) if data.get('length_of_streambank', 0) else 0
    soil_bulk_density = data.get('soil_bulk_density', 0) if data.get('soil_bulk_density', 0) else 0

    ler = lateral_erosion_rate * 0.5

    base_length = length_of_streambank
    soil_density = soil_bulk_density

    eroding_bank_height = data.get('eroding_bank_height', 0) if data.get('eroding_bank_height', 0) else 0

    square_root = math.sqrt(eroding_bank_height * eroding_bank_height)

    load_total = base_length * square_root * ler * soil_density

    soil_n_content = data.get('soil_n_content', 0) if data.get('soil_n_content', 0) else 0
    soil_p_content = data.get('soil_p_content', 0) if data.get('soil_p_content', 0) else 0

    return {
        'tn_lbs_reduced': data.get('tn_lbs_reduced', 0),
        'tp_lbs_reduced': data.get('tp_lbs_reduced', 0),
        'tss_tons_reduced': data.get('tss_tons_reduced', 0)
    }

    # return {
    #     'tn_lbs_reduced': ((load_total) / 2000) * soil_n_content,
    #     'tp_lbs_reduced': ((load_total) / 2000) * soil_p_content,
    #     'tss_tons_reduced': (load_total) / 2000
    # }


def miles_of_streambank_restored(data):

    length_of_streambank = data.get('length_of_streambank', 0) if data.get('length_of_streambank', 0) else 0

    return (length_of_streambank / 5280)
