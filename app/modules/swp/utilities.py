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

from decimal import Decimal, InvalidOperation

# Import package dependencies

from app import db
from app import logger

from app.schema.load_rates import LoadRates


CALCS = {
    'rr': {
        'tn': lambda x: (0.0308 * x ** 5) - (0.2562 * x ** 4) + (0.8634 * x ** 3) - (1.5285 * x ** 2) + (
                1.501 * x) - 0.013,
        'tp': lambda x: (0.0304 * x ** 5) - (0.2619 * x ** 4) + (0.9161 * x ** 3) - (1.6837 * x ** 2) + (
                1.7072 * x) - 0.0091,
        'tss': lambda x: (0.0326 * x ** 5) - (0.2806 * x ** 4) + (0.9816 * x ** 3) - (1.8039 * x ** 2) + (
            1.8292 * x) - 0.0091
    },
    'st': {
        'tn': lambda x: (0.0152 * x ** 5) - (0.1310 * x ** 4) + (0.4581 * x ** 3) - (0.8418 * x ** 2) + (
                0.8536 * x) - 0.0046,
        'tp': lambda x: (0.0239 * x ** 5) - (0.2058 * x ** 4) + (0.7198 * x ** 3) - (1.3229 * x ** 2) + (
                1.3414 * x) - 0.0072,
        'tss': lambda x: (0.0304 * x ** 5) - (0.2619 * x ** 4) + (0.9161 * x ** 3) - (1.6837 * x ** 2) + (
            1.7072 * x) - 0.0091
    }
}


def adjust_inches_treated(value):

    if value < 0.05:

        return 0.05

    return 2.5 % value


def tn(value):

    # =0.0308*(F5)^5-0.2562*(F5)^4+0.8634*(F5)^3-1.5285*(F5)^2+1.501*(F5)-0.013

    return (0.0308 * value ** 5) - (0.2562 * value ** 4) + (0.8634 * value ** 3) - (1.5285 * value ** 2) + (
                1.501 * value) - 0.013


def tp(value):

    # =0.0304*(F5)^5-0.2619*(F5)^4+0.9161*(F5)^3-1.6837*(F5)^2+1.7072*(F5)-0.0091

    return (0.0304 * value ** 5) - (0.2619 * value ** 4) + (0.9161 * value ** 3) - (1.6837 * value ** 2) + (
                1.7072 * value) - 0.0091


def tss(value):

    # =0.0326*(F5)^5-0.2806*(F5)^4+0.9816*(F5)^3-1.8039*(F5)^2+1.8292*(F5)-0.0098

    return (0.0326 * value ** 5) - (0.2806 * value ** 4) + (0.9816 * value ** 3) - (1.8039 * value ** 2) + (
            1.8292 * value) - 0.0091


def reduction(data):
    
    # Calculation mode.

    mode = data.get('mode')

    # Load source key.

    source_key = data.get('source_key')
    
    if not isinstance(source_key, basestring):
        
        return {}

    # Practice footprint area (acres)

    footprint_area = data.get('footprint_area')

    # Impervious acres in practice drainage area

    impervious_acres = data.get('impervious_acres')

    # Ponding depth (feet) = surface volume storage + (filter media layer * porosity)

    ponding_depth = data.get('ponding_depth')

    segments = data.get('segments')

    values = [
        footprint_area,
        impervious_acres,
        ponding_depth,
    ]

    if (not isinstance(segments, list) or
            not all(isinstance(x, (float, int)) for x in values)):

        return {}

    # Runoff storage volume (acre feet)

    runoff_storage_volume = footprint_area * ponding_depth

    logger.warning(
        'swp.utilities.reduction:runoff_storage_volume: %s.',
        runoff_storage_volume
    )

    # Runoff depth treated per impervious acres (inches)

    # Inches treated = (RunoffStorageVolume * 12) / ImperviousAcres
    # If this is below 0.05 then set to 0.05. If above 2.5 then set to 2.5.

    try:

        inches_treated = adjust_inches_treated(
            (runoff_storage_volume * 12) / impervious_acres
        )

        logger.warning(
            'swp.utilities.reduction:inches_treated: %s.',
            inches_treated
        )

        reductions = {
            'tn': CALCS[mode]['tn'](inches_treated),
            'tp': CALCS[mode]['tp'](inches_treated),
            'tss': CALCS[mode]['tss'](inches_treated)
        }

        logger.warning(
            'swp.utilities.reduction:reductions: %s.',
            reductions
        )

        return reduced_loads(
            segments,
            source_key,
            reductions
        )

    except ZeroDivisionError:

        return {}


def reduced_loads(segments, source_key, reductions):

    s_loads = []
    n_loads = []
    p_loads = []

    for segment in segments:

        rate_q = db.session.query(
            LoadRates
        ).filter(
            LoadRates.key == segment,
            LoadRates.normalized_source == source_key
        ).first()

        try:

            load_rate = rate_q.load_rate

            n_loads.append(
                rate_q.n / load_rate
            )

            p_loads.append(
                rate_q.p / load_rate
            )

            s_loads.append(
                rate_q.tss / load_rate
            )

        except (AttributeError, KeyError):

            pass

    tn_load = calc_load_reduction(n_loads, 'tn', reductions)

    tp_load = calc_load_reduction(p_loads, 'tp', reductions)

    tss_load = calc_load_reduction(s_loads, 'tss', reductions)

    return {
        'tn_lbs_reduced': tn_load,
        'tp_lbs_reduced': tp_load,
        'tss_lbs_reduced': tss_load
    }


def calc_load_reduction(loads, key, reductions):

    try:

        return (
            (sum(loads) / Decimal(len(loads))) *
            Decimal(reductions.get(key))
        )

    except InvalidOperation:

        return 0
