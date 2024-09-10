#!/usr/bin/env python

from __future__ import division

from .constants import LR_LOADS


def calculate_sediment_storage(load):
    try:
        return (load / 55) * 0.0000229569
    except (TypeError, ValueError) as error:
        return 0


def reduction(data):

    segments = data.get('segments')

    upstream_miles = data.get('upstream_miles')

    values = [
        upstream_miles,
    ]

    if (not isinstance(segments, list) or
            not all(isinstance(x, (float, int)) for x in values)):

        return {}

    s_loads = []
    n_loads = []
    p_loads = []

    for segment in segments:

        rates = LR_LOADS.get(segment)

        try:

            load_rate = rates.get('load_rate')

            n_loads.append(
                rates['n'] / load_rate
            )

            p_loads.append(
                rates['p'] / load_rate
            )

            s_loads.append(
                rates['tss'] / load_rate
            )

        except (AttributeError, KeyError):

            pass

    tn_load = (sum(n_loads) / float(len(n_loads))) * upstream_miles

    tp_load = (sum(p_loads) / float(len(p_loads))) * upstream_miles

    tss_load = (sum(s_loads) / float(len(s_loads))) * upstream_miles

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

    nitrogen_concentration = data.get('nitrogen_concentration', 0)

    nitrogen_treatment_credit = sediment_treatment_credit * nitrogen_concentration

    phosphorus_concentration = data.get('phosphorus_concentration', 0)

    phosphorus_treatment_credit = sediment_treatment_credit * phosphorus_concentration

    return {
        'tn_lbs_reduced': nitrogen_treatment_credit,
        'tp_lbs_reduced': phosphorus_treatment_credit,
        'tss_lbs_reduced': sediment_treatment_credit * 2000,
    }
