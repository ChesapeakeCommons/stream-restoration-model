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

from .constants import PRACTICE_CODES
from .constants import DEFAULT_N_CONTENT
from .constants import DEFAULT_P_CONTENT


def aggregate(unit_idx, tissue_weight_idx):
    """
    Extract model parameters and perform calculations to
    produce estimated total nitrogen and phosphorus
    content (in grams) stored by all animals in an
    oyster aquaculture conservation practice.

    :param unit_idx: A dictionary that may contain integer
    values representing the number of animals in each oyster
    size and ploidy class.
     :param tissue_weight_idx: A dictionary that may contain float
    values representing the average tissue dry weight in grams for
    each oyster size and ploidy class.
    :return: A tuple containing calculated model values
    for each target metric.
    """

    total_n_grams = 0

    total_p_grams = 0

    for code in PRACTICE_CODES:

        animal_units = unit_idx.get(code)

        default_dry_weight = tissue_weight_idx.get(code)

        if (isinstance(animal_units, int) and
                isinstance(default_dry_weight, float)):

            product = animal_units * default_dry_weight

            total_n_grams += (product * 8.2)

            total_p_grams += (product * 0.9)

    return total_n_grams, total_p_grams


def reduction(data):
    """
    Extract model parameters (using defaults if necessary)
    and perform metric-specific calculations.

    :param data: A dictionary that may contain a full set of
    float values representing variables associated with the
    physical conditions affecting an oyster aquaculture
    conservation practice.
    :return: A dictionary containing calculated model values
    for each target metric.
    """

    animal_units = data.get('animal_units')

    secondary_code = data.get('secondary_code')

    if isinstance(animal_units, int) and secondary_code in PRACTICE_CODES:

        default_n_content = DEFAULT_N_CONTENT.get(secondary_code)

        default_p_content = DEFAULT_P_CONTENT.get(secondary_code)

        # Note that 1 pound is equal to 453.59237 grams, which
        # should be used as a denominator to match the expected
        # metric units.

        return {
            'tn_lbs_reduced': (default_n_content * animal_units)/453.59237,
            'tp_lbs_reduced': (default_p_content * animal_units)/453.59237
        }

    else:

        datum = {}

        unit_idx = data.get('units')

        tissue_weight_idx = data.get('avg_tissue_dry_weight')

        if (isinstance(unit_idx, dict) and
                isinstance(tissue_weight_idx, dict)):

            total_n_grams, total_p_grams = aggregate(
                unit_idx,
                tissue_weight_idx
            )

            if total_n_grams:

                datum.update({
                    'tn_lbs_reduced': total_n_grams/453.59237
                })

            if total_p_grams:
                datum.update({
                    'tp_lbs_reduced': total_p_grams/453.59237
                })

        return datum
