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

INPUT_DEFAULTS = {
    'length_of_living_shoreline': 1000.0,
    'existing_average_bank_height': 4.0,
    'existing_shoreline_recession_rate': 1.0,
    'soil_bulk_density': 93.6,
    'sand_reduction_factor': 0.551,
    'bank_instability_reduction_factor': 1.0,
    'planted_tidal_wetland_area': 0.25
}

STATE_COEFFICIENTS = {
    'n': {
        'dc': lambda a: a * 0.04756,
        'de': lambda a: a * 0.04756,
        'md': lambda a: a * 0.04756,
        'va': lambda a: a * 0.01218
    },
    'p': {
        'dc': lambda a: a * 0.03362,
        'de': lambda a: a * 0.03362,
        'md': lambda a: a * 0.03362,
        'va': lambda a: a * 0.00861
    },
    'tss': {
        'dc': lambda a: (164*a)/2000,
        'de': lambda a: (164*a)/2000,
        'md': lambda a: (164*a)/2000,
        'va': lambda a: (42*a)/2000
    }
}