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

from .constants import LR_LOADS


def reduction(data):

    existing_treated_discharge = data.get('existing_treated_discharge')

    proposed_treated_discharge = data.get('proposed_treated_discharge')

    existing_total_discharge = data.get('existing_total_discharge')

    proposed_total_discharge = data.get('proposed_total_discharge')

    values = [
        existing_treated_discharge,
        proposed_treated_discharge,
        existing_total_discharge,
        proposed_total_discharge,
    ]

    if not all(isinstance(x, (float, int)) for x in values):

        return {}

    existing_percent_flow_treated = (
        float(existing_treated_discharge) /
        float(existing_total_discharge)
    )

    proposed_percent_flow_treated = (
        float(proposed_treated_discharge) /
        float(proposed_total_discharge)
    )

    treatable_flow_credit = (
        proposed_percent_flow_treated -
        existing_percent_flow_treated
    )

    return {
        'existing_percent_flow_treated': existing_percent_flow_treated,
        'proposed_percent_flow_treated': proposed_percent_flow_treated,
        'treatable_flow_credit': treatable_flow_credit
    }
