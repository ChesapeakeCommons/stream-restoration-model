#!/usr/bin/env python

"""Define the Stormwater schema.

Created by Viable Industries, L.L.C. on 02/05/2017.
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

PRACTICE_CODES = [
    'diploid_225',
    'diploid_3',
    'diploid_4',
    'diploid_5',
    'diploid_gt_6',
    'triploid_225',
    'triploid_3',
    'triploid_4',
    'triploid_5',
    'triploid_gt_6'
]

DEFAULT_DRY_WEIGHT = {
    'diploid_225': 0.63,
    'diploid_3': 1.06,
    'diploid_4': 1.81,
    'diploid_5': 2.70,
    'diploid_gt_6': 3.74,
    'triploid_225': 0.79,
    'triploid_3': 1.56,
    'triploid_4': 3.16,
    'triploid_5': 5.33,
    'triploid_gt_6': 8.20
}

DEFAULT_N_CONTENT = {
    'diploid_225': 0.05,
    'diploid_3': 0.09,
    'diploid_4': 0.15,
    'diploid_5': 0.22,
    'diploid_gt_6': 0.31,
    'triploid_225': 0.06,
    'triploid_3': 0.13,
    'triploid_4': 0.26,
    'triploid_5': 0.44,
    'triploid_gt_6': 0.67
}

DEFAULT_P_CONTENT = {
    'diploid_225': 0.01,
    'diploid_3': 0.01,
    'diploid_4': 0.02,
    'diploid_5': 0.02,
    'diploid_gt_6': 0.03,
    'triploid_225': 0.01,
    'triploid_3': 0.01,
    'triploid_4': 0.03,
    'triploid_5': 0.05,
    'triploid_gt_6': 0.07
}
