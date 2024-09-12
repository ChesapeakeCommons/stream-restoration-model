#!/usr/bin/env python

from __future__ import division

from decimal import Decimal
from decimal import DivisionUndefined
from decimal import DivisionByZero
from decimal import InvalidOperation

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

EFFICIENCY_REDUCTIONS = {
    'dry_pond': {
        'tn': lambda x: 0.05,
        'tp': lambda x: 0.10,
        'tss': lambda x: 0.10,
    },
    'dry_extended_detention_pond': {
        'tn': lambda x: 0.20,
        'tp': lambda x: 0.20,
        'tss': lambda x: 0.60,
    },
    'runoff_reduction': {
        'tn': lambda x: CALCS['rr']['tn'](x),
        'tp': lambda x: CALCS['rr']['tp'](x),
        'tss': lambda x: CALCS['rr']['tss'](x),
    },
    'wet_pond': {
        'tn': lambda x: CALCS['st']['tn'](x),
        'tp': lambda x: CALCS['st']['tp'](x),
        'tss': lambda x: CALCS['st']['tss'](x),
    },
}


def adjust_inches_treated(value):
    return 0.05 if value < 0.05 else min(value, 2.5)


def validate_load_sources(data):
    load_sources = data.get('load_sources', [])

    return (
        isinstance(load_sources, list) and
        len(load_sources) > 0
    )


def reduction(data):
    # Land river segment list.

    segments = data.get('segments')

    if not isinstance(segments, list):
        return data

    if not validate_load_sources(data):
        return get_load_sources(segments, data)

    input_groups = data.get('input_groups', [])

    if not isinstance(input_groups, list):
        return data

    # Calculation mode.

    mode = data.get('mode', 'rr')

    if mode not in ['rr', 'st']:
        return data

    existing_bmp = data.get('existing_bmp')

    if existing_bmp is not None:
        existing_bmp = process_existing_bmp(existing_bmp)

    calculate_inches_treated(data)

    for group in input_groups:
        try:
            process_input_group(
                segments,
                group,
                data,
                existing_bmp,
            )
        except ValueError:
            pass

    keys = [
        'tn_lbs_reduced',
        'tp_lbs_reduced',
        'tss_lbs_reduced',
    ]

    for key in keys:
        data[key] = sum(group.get(key) for group in input_groups)

    data['existing_bmp'] = existing_bmp

    return data


def calculate_inches_treated(spec):
    # Practice footprint area (acres)

    footprint_area = data.get('footprint_area', 0.0)

    # Impervious acres in practice drainage area

    impervious_acres = data.get('impervious_acres', 1.0)

    # Ponding depth (feet) = surface volume storage + (filter media layer * porosity)

    ponding_depth = data.get('ponding_depth', 0.0)

    # Runoff storage volume (acre feet)

    runoff_storage_volume = footprint_area * ponding_depth

    logger.warning(
        'swp.utilities.calculate_inches_treated.runoff_storage_volume: %s.',
        runoff_storage_volume
    )

    treatment_depth = runoff_storage_volume * 12

    try:
        inches_treated = adjust_inches_treated(
            treatment_depth / impervious_acres
        )

        logger.warning(
            'swp.utilities.calculate_inches_treated.inches_treated: %s.',
            inches_treated
        )

        spec.update({
            'runoff_storage_volume': runoff_storage_volume,
            'treatment_depth': treatment_depth,
            'inches_treated': inches_treated,
        })

        return spec

    except ZeroDivisionError:
        return spec


def process_existing_bmp(data):
    calculate_inches_treated(data)

    inches_treated = data.get('inches_treated', 0.0)

    logger.warning(
        'swp.utilities.process_existing_bmp.inches_treated: %s.',
        inches_treated
    )

    bmp_type = data.get('bmp_type')

    data.update({
        'tn_efficiency_reduction': EFFICIENCY_REDUCTIONS[bmp_type]['tn'](inches_treated),
        'tp_efficiency_reduction': EFFICIENCY_REDUCTIONS[bmp_type]['tp'](inches_treated),
        'tss_efficiency_reduction': EFFICIENCY_REDUCTIONS[bmp_type]['tss'](inches_treated),
    })

    return data


def process_input_group(
    segments,
    group,
    data,
    existing_bmp=None,
):
    # Load source key.

    source_key = group.get('source_key')

    if not isinstance(source_key, basestring):
        return data

    inches_treated = data.get('inches_treated', 0.0)

    logger.warning(
        'swp.utilities.process_input_group:inches_treated: %s.',
        inches_treated
    )

    tn_pct_reduced = CALCS[mode]['tn'](inches_treated)
    tp_pct_reduced = CALCS[mode]['tp'](inches_treated)
    tss_pct_reduced = CALCS[mode]['tss'](inches_treated)

    if existing_bmp:
        tn_pct_reduced -= existing_bmp.get('tn_efficiency_reduction')
        tp_pct_reduced -= existing_bmp.get('tp_efficiency_reduction')
        tss_pct_reduced -= existing_bmp.get('tss_efficiency_reduction')

    group.update({
        'tn_pct_reduced': tn_pct_reduced,
        'tp_pct_reduced': tn_pct_reduced,
        'tss_pct_reduced': tss_pct_reduced,
    })

    logger.warning(
        'swp.utilities.process_input_group:reductions: %s.',
        group
    )

    calc_reduced_loads(
        segments,
        source_key,
        group,
        data,
    )


def calculate_constituent_load(constituent_rate, base_rate,):
    try:
        return constituent_rate / base_rate
    except (
        TypeError,
        ValueError,
        ZeroDivisionError,
        DivisionByZero,
        DivisionUndefined,
        InvalidOperation
    ):
        return 0.0


def calc_reduced_loads(
    segments,
    source_key,
    group,
    data,
):
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
                calculate_constituent_load(
                    constituent_rate=rate_q.n,
                    base_rate=load_rate,
                )
            )

            p_loads.append(
                calculate_constituent_load(
                    constituent_rate=rate_q.p,
                    base_rate=load_rate,
                )
            )

            s_loads.append(
                calculate_constituent_load(
                    constituent_rate=rate_q.tss,
                    base_rate=load_rate,
                )
            )
        except (AttributeError, KeyError):
            pass

    red_credits = {
        'tn': calc_load_reduction(
            loads=n_loads,
            key='tn_pct_reduced',
            group=group,
        ),
        'tp': calc_load_reduction(
            loads=p_loads,
            key='tp_pct_reduced',
            group=group,
        ),
        'tss': calc_load_reduction(
            loads=s_loads,
            key='tss_pct_reduced',
            group=group,
        )
    }

    group.update({
        'tn_lbs_reduced': red_credits.get('tn'),
        'tp_lbs_reduced': red_credits.get('tp'),
        'tss_lbs_reduced': red_credits.get('tss'),
    })

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


def calc_load_reduction(loads, key, group):
    try:
        # Load rate (pounds/acre)

        segment_avg_load = sum(loads) / Decimal(len(loads))

        # Pre-restoration load (pounds/acre)

        pre_load = segment_avg_load * Decimal(group.get('source_acres', 0.0))

        return pre_load * Decimal(group.get(key))

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
        LoadRates.normalized_source != 'regulated_construction',
        LoadRates.normalized_source != 'css_construction'
    ).order_by(
        LoadRates.source
    ).distinct(
        LoadRates.source
    )

    data.update({
        'load_sources': [row._asdict() for row in rate_q]
    })

    return data
