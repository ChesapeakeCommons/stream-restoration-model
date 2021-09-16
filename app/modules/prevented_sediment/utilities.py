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

    bulk_density_of_soil = data.get('bulk_density_of_soil', 0)

    bank_erosion_rate = data.get('bank_erosion_rate', 0)

    eroding_bank_area = data.get('eroding_bank_area', 0)

    if (isinstance(bulk_density_of_soil, (float, int)) and
            isinstance(bank_erosion_rate, (float, int)) and
            isinstance(eroding_bank_area, (float, int))):

        operands = [
            bulk_density_of_soil,
            bank_erosion_rate,
            eroding_bank_area,
            0.50
        ]

        return {
            'tss_lbs_reduced': reduce(lambda x, y: x*y, operands)
        }

    return {}
