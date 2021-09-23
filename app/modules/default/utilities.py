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

    length_of_streambank = data.get('length_of_streambank')

    if isinstance(length_of_streambank, (float, int)):

        return {
            'tn_lbs_reduced': length_of_streambank * 0.075,
            'tp_lbs_reduced': length_of_streambank * 0.068,
            'tss_lbs_reduced': length_of_streambank * 248.0
        }

    return {}
