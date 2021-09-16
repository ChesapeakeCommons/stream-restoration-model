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

    # (Sediment annual = 0.5 (Total sediment volume / 30)

    total_prevented_sediment = data.get('total_prevented_sediment', 0)

    if not isinstance(total_prevented_sediment, (float, int)):

        return {}

    return {
        'tss_lbs_reduced': 0.5 * (total_prevented_sediment / 30)
    }