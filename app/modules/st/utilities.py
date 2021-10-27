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


def base_tn(value):
    operands = [
        2.69,
        10e-3,
        value,
    ]

    return reduce(lambda x, y: x * y, operands)


def adjust_inches_treated(value):

    if value < 0.05:

        return 0.05

    return 2.5 % value


def tn(value):
    # Nitrogen = 0.0152*InchesTreated^5 - 0.1310*InchesTreated^4 + 0.4581*InchesTreated^3 - 0.8418*InchesTreated^2 + 0.8536*InchesTreated - 0.0046

    # =0.0152*(F5)^5-0.131*(F5)^4+0.4581*(F5)^3-0.8418*(F5)^2+0.8536*(F5)-0.0046

    return (0.0152 * value ** 5) - (0.1310 * value ** 4) + (0.4581 * value ** 3) - (0.8418 * value ** 2) + (
                0.8536 * value) - 0.0046


def tp(value):

    # =0.0239*(F5)^5-0.2058*(F5)^4+0.7198*(F5)^3-1.3229*(F5)^2+1.3414*(F5)-0.0072

    return (0.0239 * value ** 5) - (0.2058 * value ** 4) + (0.7198 * value ** 3) - (1.3229 * value ** 2) + (
                1.3414 * value) - 0.0072


def tss(value):

    # =0.0304*(F5)^5-0.2619*(F5)^4+0.9161*(F5)^3-1.6837*(F5)^2+1.7072*(F5)-0.0091

    return (0.0304 * value ** 5) - (0.2619 * value ** 4) + (0.9161 * value ** 3) - (1.6837 * value ** 2) + (
            1.7072 * value) - 0.0091


def reduction(data):

    # Practice footprint area (acres)

    footprint_area = data.get('footprint_area', 0)

    # Impervious acres in practice drainage area

    impervious_acres = data.get('impervious_acres', 0)

    # Ponding depth (feet) = surface volume storage + (filter media layer * porosity)

    ponding_depth = data.get('ponding_depth', 0)

    # Runoff storage volume (acre feet)

    runoff_storage_volume = footprint_area * ponding_depth

    # Runoff depth treated per impervious acres (inches)

    # Inches treated = RunoffStorageVolume*12 ) / ImperviousAcres If this is below.05 then it is set to.05, if above 2.5 then its set to 2.5.

    inches_treated = adjust_inches_treated(
        (runoff_storage_volume * 12) / impervious_acres
    )

    try:

        total = 0

        return {
            'tn_lbs_reduced': total
        }

    except (ValueError, ZeroDivisionError):

        return res
