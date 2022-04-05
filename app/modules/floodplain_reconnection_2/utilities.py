#!/usr/bin/env python



from .constants import LR_LOADS


def reduction(data):

    segments = data.get('segments')

    upstream_miles = data.get('upstream_miles')

    treatable_flow_credit = data.get('treatable_flow_credit')

    values = [
        upstream_miles,
        treatable_flow_credit,
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

    return {
        'tn_load': tn_load,
        'tp_load': tp_load,
        'tss_load': tss_load,
        'tn_treatable_load': tn_load * treatable_flow_credit,
        'tp_treatable_load': tp_load * treatable_flow_credit,
        'tss_treatable_load': tss_load * treatable_flow_credit
    }
