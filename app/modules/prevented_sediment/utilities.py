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

from __future__ import division

import math
from datetime import datetime

# Import package dependencies

from app import logger


def reduction(data):

    banks = data.get('banks', [])

    if not isinstance(banks, list):

        return {}

    idx = {
        'tn_lbs_reduced': 0,
        'tp_lbs_reduced': 0,
        'tss_lbs_reduced': 0
    }

    for bank in banks:

        try:

            process_bank(bank, idx)

        except ValueError:

            pass

    return {key: value * 0.5 for key, value in idx.iteritems()}


def process_bank(data, idx):

    bulk_density_of_soil = data.get('bulk_density_of_soil', 0)

    bank_erosion_rate = data.get('bank_erosion_rate', 0)

    eroding_bank_length = data.get('eroding_bank_length', 0)

    eroding_bank_height = data.get('eroding_bank_height', 0)

    nitrogen_concentration = data.get('nitrogen_concentration', 0)

    phosphorus_concentration = data.get('phosphorus_concentration', 0)

    values = [
        bulk_density_of_soil,
        bank_erosion_rate,
        eroding_bank_height,
        eroding_bank_length,
        nitrogen_concentration,
        phosphorus_concentration,
    ]

    if not all(isinstance(x, (float, int)) for x in values):

        raise ValueError('Missing required inputs.')

    operands = [
        bulk_density_of_soil,
        bank_erosion_rate,
        eroding_bank_length,
        eroding_bank_height
    ]

    tss_lbs_reduced = reduce(lambda x, y: x * y, operands)

    tn_lbs_reduced = tss_lbs_reduced * nitrogen_concentration

    tp_lbs_reduced = tss_lbs_reduced * phosphorus_concentration

    idx['tss_lbs_reduced'] += tss_lbs_reduced

    idx['tn_lbs_reduced'] += tn_lbs_reduced

    idx['tp_lbs_reduced'] += tp_lbs_reduced
