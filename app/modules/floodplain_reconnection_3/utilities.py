#!/usr/bin/env python

EFF = {
    "restoration": {
        "tn": 0.42,
        "tp": 0.4,
        "tss": 0.31
    },
    "creation": {
        "tn": 0.3,
        "tp": 0.33,
        "tss": 0.27
    },
    "rehab": {
        "tn": 0.16,
        "tp": 0.22,
        "tss": 0.19
    }
}


def reduction(data):

    tn_treatable_load = data.get('tn_treatable_load')

    tp_treatable_load = data.get('tp_treatable_load')

    tss_treatable_load = data.get('tss_treatable_load')

    wetland_restoration = data.get('wetland_restoration', 0)

    wetland_creation = data.get('wetland_creation', 0)

    wetland_rehab = data.get('wetland_rehab', 0)

    values = [
        tn_treatable_load,
        tp_treatable_load,
        tss_treatable_load,
        wetland_restoration,
        wetland_creation,
        wetland_rehab,
    ]

    if not all(isinstance(x, (float, int)) for x in values):

        return {
            'tn_lbs_reduced': 0,
            'tp_lbs_reduced': 0,
            'tss_lbs_reduced': 0
        }

    tn = []
    tp = []
    tss = []

    for key, value in EFF.iteritems():

        tn.append(
            value['tn'] * tn_treatable_load
        )

        tp.append(
            value['tp'] * tp_treatable_load
        )

        tss.append(
            value['tss'] * tss_treatable_load
        )

    return {
        'tn_lbs_reduced': sum(tn),
        'tp_lbs_reduced': sum(tp),
        'tss_lbs_reduced': sum(tss)
    }
