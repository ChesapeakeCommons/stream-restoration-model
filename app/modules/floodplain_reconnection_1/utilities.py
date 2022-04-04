#!/usr/bin/env python


def reduction(data):

    existing_treated_discharge = data.get('existing_treated_discharge')

    proposed_treated_discharge = data.get('proposed_treated_discharge')

    existing_total_discharge = data.get('existing_total_discharge')

    proposed_total_discharge = data.get('proposed_total_discharge')

    values = [
        existing_treated_discharge,
        proposed_treated_discharge,
        existing_total_discharge,
        proposed_total_discharge,
    ]

    if not all(isinstance(x, (float, int)) for x in values):

        return {}

    existing_percent_flow_treated = (
        float(existing_treated_discharge) /
        float(existing_total_discharge)
    )

    proposed_percent_flow_treated = (
        float(proposed_treated_discharge) /
        float(proposed_total_discharge)
    )

    treatable_flow_credit = (
        proposed_percent_flow_treated -
        existing_percent_flow_treated
    )

    return {
        'existing_percent_flow_treated': existing_percent_flow_treated,
        'proposed_percent_flow_treated': proposed_percent_flow_treated,
        'treatable_flow_credit': treatable_flow_credit
    }
