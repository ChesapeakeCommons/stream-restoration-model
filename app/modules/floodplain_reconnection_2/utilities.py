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

    segments = data.get('segments')

    upstream_miles = data.get('upstream_miles')

    treatable_flow_credit = data.get('treatable_flow_credit')

    values = [
        upstream_miles,
        treatable_flow_credit,
    ]

    if (not isinstance(segments, list) or
            not all(isinstance(x, (float, int)) for x in values)):

        return {}

    s_loads = []
    n_loads = []
    p_loads = []

    for segment in segments:

        rates = LR_LOADS.get(segment)

        try:

            load_rate = rates.get('load_rate')

            n_loads.append(
                rates['n'] / load_rate
            )

            p_loads.append(
                rates['p'] / load_rate
            )

            s_loads.append(
                rates['tss'] / load_rate
            )

        except (AttributeError, KeyError):

            pass

    tn_load = sum(n_loads) / float(len(n_loads)) * upstream_miles,
    tp_load = sum(p_loads) / float(len(p_loads)) * upstream_miles,
    tss_load = sum(s_loads) / float(len(s_loads)) * upstream_miles

    return {
        'tn_load': tn_load,
        'tp_load': tp_load,
        'tss_load': tss_load,
        'tn_treatable_load': tn_load * treatable_flow_credit,
        'tp_treatable_load': tp_load * treatable_flow_credit,
        'tss_treatable_load': tss_load * treatable_flow_credit
    }
