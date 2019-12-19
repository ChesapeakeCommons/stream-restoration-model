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

import functools
import operator

# Import package dependencies

from app import logger

# Import module dependencies

from .constants import STATE_COEFFICIENTS


# Protocol 1: Erosion Prevention


def tn_1(grams, percent_n):
    """
    Multiply a list of values and multiply the product
    by a standard coefficient.

    :param seq: A list of numeric values representing
    variables associated with the physical conditions
    affecting a shoreline management conservation
    practice.
    :return: A float value representing the estimated
    total nitrogen load reduction in pounds produced
    by the given input variable values.
    """

    if (isinstance(grams, (float, int)) and
            isinstance(percent_n, (float, int))):

        return (grams * (percent_n / 100)) / 0.0022

    return 0


def tp_1(grams, percent_p):
    """
    Multiply a list of values and multiply the product
    by a standard coefficient.

    :param seq: A list of numeric values representing
    variables associated with the physical conditions
    affecting a shoreline management conservation
    practice.
    :return: A float value representing the estimated
    total nitrogen load reduction in pounds produced
    by the given input variable values.
    """

    if (isinstance(grams, (float, int)) and
            isinstance(percent_p, (float, int))):

        return (grams * (percent_p / 100)) / 0.0022

    return 0


def tss_1(grams, percent_solids):
    """
    Multiply a list of values and divide the product
    by 2,000 (pounds per ton).

    :param seq: A list of numeric values representing
    variables associated with the physical conditions
    affecting a shoreline management conservation
    practice.
    :return: A float value representing the estimated
    total suspended solids load reduction in tons
    produced by the given input variable values.
    """

    if (isinstance(grams, (float, int)) and
            isinstance(percent_solids, (float, int))):

        return ((grams * (percent_solids / 100.0)) / 0.0022) / 2000

    return 0


def reduction(data):
    """
    Extract model parameters (using defaults if necessary)
    and perform metric-specific calculations.

    :param data: A dictionary that may contain a full set of
    float values representing variables associated with the
    physical conditions affecting an algal flow-way
    conservation practice.
    :return: A dictionary containing calculated model values
    for each target metric.
    """

    secondary_code = data.get('secondary_code')

    if secondary_code == 'monitored':

        return {
            'tn_lbs_reduced': tn_1(
                grams=data.get('biomass'),
                percent_n=data.get('percent_n')
            ),
            'tp_lbs_reduced': tp_1(
                grams=data.get('biomass'),
                percent_p=data.get('percent_p')
            ),
            'tss_tons_reduced': tss_1(
                grams=data.get('biomass'),
                percent_solids=data.get('percent_ash_solids')
            )
        }

    surface_area = data.get('surface_area')

    if isinstance(surface_area, (float, int)):

        return {
            'tn_lbs_reduced': surface_area * 545,
            'tp_lbs_reduced': surface_area * 45,
            'tss_tons_reduced': (surface_area * 3219) / 2000
        }

    return {}
