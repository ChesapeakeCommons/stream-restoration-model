#!/usr/bin/env python

from __future__ import division

import contextlib

from .constants import LR_LOADS


def calculate_load(
    loads,
    upstream_miles,
):
    try:
        return (sum(loads) / float(len(loads))) * upstream_miles
    except (
        AttributeError,
        TypeError,
        ValueError,
        ZeroDivisionError,
    ):
        return 0


def calculate_sediment_storage(load):
    try:
        return (load / 55) * 0.0000229569
    except (TypeError, ValueError) as error:
        return 0


def cap_load_reduction(
    total_treatable_load,
    treatment_credit,
):
    return min(treatment_credit, total_treatable_load)


def reduction(data):

    segments = data.get('segments')

    upstream_miles = data.get('upstream_miles')

    values = [
        upstream_miles,
    ]

    if (not isinstance(segments, list) or
            not all(isinstance(x, (float, int)) for x in values)):
        return {}

    sediment_loads = []
    nitrogen_loads = []
    phosphorus_loads = []

    for segment in segments:

        rates = LR_LOADS.get(segment)

        with contextlib.suppress(AttributeError, KeyError):
            load_rate = rates.get('load_rate', 1)
            nitrogen_loads.append(
                rates['n'] / load_rate
            )
            phosphorus_loads.append(
                rates['p'] / load_rate
            )
            sediment_loads.append(
                rates['tss'] / load_rate
            )

    tn_load = calculate_load(nitrogen_loads, upstream_miles)

    tp_load = calculate_load(phosphorus_loads, upstream_miles)

    tss_load = calculate_load(sediment_loads, upstream_miles)

    annual_sediment_volume = calculate_sediment_storage(tss_load)

    existing_floodplain_trapping_zone_area = data.get('existing_floodplain_trapping_zone_area', 0)

    existing_floodplain_storage = (existing_floodplain_trapping_zone_area * 0.33) / 12

    proposed_floodplain_trapping_zone_area = data.get('proposed_floodplain_trapping_zone_area', 0)

    proposed_floodplain_storage = (proposed_floodplain_trapping_zone_area * 0.33) / 12

    existing_floodplain_storage_effectiveness = existing_floodplain_storage / annual_sediment_volume

    proposed_floodplain_storage_effectiveness = proposed_floodplain_storage / annual_sediment_volume

    pre_restoration_treatable_flow = data.get('pre_restoration_treatable_flow', 0)

    existing_treatment = (tss_load * existing_floodplain_storage_effectiveness * pre_restoration_treatable_flow) / 2000

    post_restoration_treatable_flow = data.get('post_restoration_treatable_flow', 0)

    proposed_treatment = (tss_load * proposed_floodplain_storage_effectiveness * post_restoration_treatable_flow) / 2000

    sediment_treatment_credit = proposed_treatment - existing_treatment

    nitrogen_concentration = data.get('nitrogen_concentration', 4.82)

    nitrogen_treatment_credit = sediment_treatment_credit * nitrogen_concentration

    phosphorus_concentration = data.get('phosphorus_concentration', 1.13)

    phosphorus_treatment_credit = sediment_treatment_credit * phosphorus_concentration

    return {
        'tn_lbs_reduced': cap_load_reduction(
            total_treatable_load=tn_load,
            treatment_credit=nitrogen_treatment_credit,
        ),
        'tp_lbs_reduced': cap_load_reduction(
            total_treatable_load=tp_load,
            treatment_credit=phosphorus_treatment_credit,
        ),
        'tss_lbs_reduced': cap_load_reduction(
            total_treatable_load=tss_load,
            treatment_credit=(sediment_treatment_credit * 2000),
        )
    }
