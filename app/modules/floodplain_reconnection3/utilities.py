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

EFF = {
    "restoration": {
        "tn": 0.42,
        "tp": 0.4,
        "tss": 0.31
    },
    "creation": {
        "tn": 0.3,
        "tp": 0.33,
        "tss": 0.27
    },
    "rehab": {
        "tn": 0.16,
        "tp": 0.22,
        "tss": 0.19
    }
}


def reduction(data):

    tn_treatable_load = data.get('tn_treatable_load')

    tp_treatable_load = data.get('tp_treatable_load')

    tss_treatable_load = data.get('tss_treatable_load')

    wetland_restoration = data.get('wetland_restoration', 0)

    wetland_creation = data.get('wetland_creation', 0)

    wetland_rehab = data.get('wetland_rehab', 0)

    values = [
        tn_treatable_load,
        tp_treatable_load,
        tss_treatable_load,
        wetland_restoration,
        wetland_creation,
        wetland_rehab,
    ]

    if not all(isinstance(x, (float, int)) for x in values):

        return {}

    tn = []
    tp = []
    tss = []

    for key, value in EFF.iteritems():

        tn.append(
            value['tn'] * tn_treatable_load
        )

        tp.append(
            value['tp'] * tp_treatable_load
        )

        tss.append(
            value['tss'] * tss_treatable_load
        )

    return {
        'tn_lbs_reduced': sum(tn),
        'tp_lbs_reduced': sum(tp),
        'tss_lbs_reduced': sum(tss)
    }
