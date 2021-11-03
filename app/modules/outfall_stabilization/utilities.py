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
            'tn_lbs_reduced': data.get('tn_lbs_reduced', 0),
            'tp_lbs_reduced': data.get('tp_lbs_reduced', 0),
            'tss_tons_reduced': data.get('tss_tons_reduced', 0)
        }

    else:

        return {
            'tn_lbs_reduced': nitrogen(data),
            'tp_lbs_reduced': phosphorus(data),
            'tss_tons_reduced': sediment(data)
        }


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
