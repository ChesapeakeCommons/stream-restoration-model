#!/usr/bin/env python

import math


def reduction(data):

    """If the measurement_period is Pre-Installation the LER will use the
    raw lateral_erosion_rate provided by the user.

    If the measurement_period is Planning or Installation the LER will be
    halved (i.e., multipled by 0.5).

    The Expert Panel (EP) guidance specifies a default value of 50%,
    subject to post-installation monitoring which could justify a larger
    reduction efficiency.[1]

    [1] Gene Yagow, Senior Research Scientist, Biological Systems
        Engineering Department Virginia Tech
    """

    has_majority_design_completion = data.get('has_majority_design_completion', False)

    length_of_streambank = data.get('length_of_streambank', 0)

    if isinstance(length_of_streambank, (float, int)):

        if has_majority_design_completion:

            lateral_erosion_rate = data.get('lateral_erosion_rate', 0)

            soil_bulk_density = data.get('soil_bulk_density', 0)

            ler = lateral_erosion_rate * 0.5

            base_length = length_of_streambank
            soil_density = soil_bulk_density

            eroding_bank_height = data.get('eroding_bank_height', 0)

            square_root = math.sqrt(eroding_bank_height * eroding_bank_height)

            load_total = base_length * square_root * ler * soil_density

            soil_n_content = data.get('soil_n_content', 0)
            soil_p_content = data.get('soil_p_content', 0)

            return {
                'tn_lbs_reduced': (load_total / 2000) * soil_n_content,
                'tp_lbs_reduced': (load_total / 2000) * soil_p_content,
                'tss_tons_reduced': load_total / 2000
            }

        return {
            'tn_lbs_reduced': length_of_streambank * 0.075,
            'tp_lbs_reduced': length_of_streambank * 0.068,
            'tss_tons_reduced': (float(length_of_streambank) * 248) / 2000
        }

    return {}
