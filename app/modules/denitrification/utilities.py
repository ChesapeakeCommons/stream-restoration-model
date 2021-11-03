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

from __future__ import division

import math as Math
from datetime import datetime

# Import package dependencies

from app import logger

# Import module dependencies

from .constants import URBAN_STATE_UAL as load_data


def base_tn(value):

    operands = [
        2.69,
        10e-3,
        value,
    ]

    return reduce(lambda x, y: x*y, operands)


def reduction(data):

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
        acrf
    ]

    res = {
        'tn_lbs_reduced': 0
    }

    if not all(isinstance(x, (float, int)) for x in values):

        return res

    floodplain_tn = base_tn(floodplain_sq_ft)

    channel_tn = base_tn(channel_sq_ft)

    discount_factors = [brf, fhf, acrf]

    denominator = reduce(lambda x, y: x*y, discount_factors)

    try:

        total = (floodplain_tn / denominator) + (channel_tn / denominator)

        return {
            'tn_lbs_reduced': total
        }

    except (ValueError, ZeroDivisionError):

        return res
