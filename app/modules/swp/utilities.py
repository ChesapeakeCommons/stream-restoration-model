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

from __future__ import division

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

    # Land river segment list.

    segments = data.get('segments')

    if not isinstance(segments, list):

        return data

    if not isinstance(data.get('load_sources'), list):

        return get_load_sources(segments, data)

    input_groups = data.get('input_groups', [])

    if not isinstance(input_groups, list):

        return {}

    for group in input_groups:

        try:

            process_input_group(segments, group, data)

        except ValueError:

            pass

    keys = [
        'tss_lbs_reduced',
        'tn_lbs_reduced',
        'tss_lbs_reduced'
    ]

    for key in keys:

        data[key] = sum(group.get(key) for group in input_groups)

    return data


def process_input_group(segments, group, data):

    # Load source key.

    source_key = group.get('source_key')

    if not isinstance(source_key, basestring):

        raise ValueError('Missing valid `source_key`.')

    # Practice footprint area (acres)

    footprint_area = group.get('footprint_area')

    # Impervious acres in practice drainage area

    impervious_acres = group.get('impervious_acres')

    # Ponding depth (feet) = surface volume storage + (filter media layer * porosity)

    ponding_depth = group.get('ponding_depth')

    values = [
        footprint_area,
        impervious_acres,
        ponding_depth,
    ]

    # Calculation mode.

    mode = data.get('mode', 'rr')

    if (mode not in ['rr', 'st'] or
            not all(isinstance(x, (float, int)) for x in values)):

        raise ValueError('Invalid mode or numeric inputs.')

    # Runoff storage volume (acre feet)

    runoff_storage_volume = footprint_area * ponding_depth

    logger.warning(
        'swp.utilities.process_input_group:runoff_storage_volume: %s.',
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
            'swp.utilities.process_input_group:inches_treated: %s.',
            inches_treated
        )

        group.update({
            'tn_pct_reduced': CALCS[mode]['tn'](inches_treated),
            'tp_pct_reduced': CALCS[mode]['tp'](inches_treated),
            'tss_pct_reduced': CALCS[mode]['tss'](inches_treated)
        })

        logger.warning(
            'swp.utilities.process_input_group:reductions: %s.',
            group
        )

        calc_reduced_loads(
            segments,
            source_key,
            group,
            data
        )

    except ZeroDivisionError as error:

        raise ValueError(error.message)


def calc_reduced_loads(segments, source_key, group, data):

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

    red_credits = {
        'tn': calc_load_reduction(
            n_loads,
            'tn_pct_reduced',
            group
        ),
        'tp': calc_load_reduction(
            p_loads,
            'tp_pct_reduced',
            group
        ),
        'tss': calc_load_reduction(
            s_loads,
            'tss_pct_reduced',
            group
        )
    }

    group.update({
        'tn_lbs_reduced': red_credits.get('tn'),
        'tp_lbs_reduced': red_credits.get('tp'),
        'tss_lbs_reduced': red_credits.get('tss')
    })

    # keys = [
    #     'tss_lbs_reduced',
    #     'tn_lbs_reduced',
    #     'tss_lbs_reduced'
    # ]
    #
    # for key in keys:
    #
    #     prefix = key.split('_')[0]
    #
    #     set_total(data, key, red_credits.get(prefix))

    return data


def set_total(data, key, value):

    existing_value = data.get(key)

    if not isinstance(existing_value, (float, int, Decimal)):

        existing_value = Decimal(0)

    else:

        existing_value = Decimal(existing_value)

    data[key] = existing_value + Decimal(value)


def set_default(data, key, default=0):

    value = data.get(key)

    if not isinstance(value, (float, int, Decimal)):

        data[key] = default

    return data


def calc_load_reduction(loads, key, reductions):

    try:

        return (
            (sum(loads) / Decimal(len(loads))) *
            Decimal(reductions.get(key))
        )

    except InvalidOperation:

        return 0


def get_load_sources(segments, data):

    if not isinstance(segments, list) or not isinstance(data, dict):

        return data

    rate_q = db.session.query(
        LoadRates.source.label('name'),
        LoadRates.normalized_source.label('key')
    ).filter(
        LoadRates.key.in_(segments),
        LoadRates.normalized_source != 'regulated_construction'
    ).order_by(
        LoadRates.source
    ).distinct(
        LoadRates.source
    )

    data.update({
        'load_sources': [row._asdict() for row in rate_q]
    })

    return data
