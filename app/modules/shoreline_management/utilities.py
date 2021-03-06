#!/usr/bin/env python

from app.utilities import product

from .constants import STATE_COEFFICIENTS


# Protocol 1: Erosion Prevention


def tn_1(seq):
    """
    Multiply a list of values and multiply the product
    by a standard coefficient.

    :param seq: A list of numeric values representing
    variables associated with the physical conditions
    affecting a shoreline management conservation
    practice.
    :return: A float value representing the estimated
    total nitrogen load reduction in pounds produced
    by the given input variable values.
    """

    return product(seq) * 0.00029


def tp_1(seq):
    """
    Multiply a list of values and multiply the product
    by a standard coefficient.

    :param seq: A list of numeric values representing
    variables associated with the physical conditions
    affecting a shoreline management conservation
    practice.
    :return: A float value representing the estimated
    total phosphorus load reduction in pounds produced
    by the given input variable values.
    """

    return product(seq) * 0.000205


def tss_1(seq):
    """
    Multiply a list of values and divide the product
    by 2,000 (pounds per ton).

    :param seq: A list of numeric values representing
    variables associated with the physical conditions
    affecting a shoreline management conservation
    practice.
    :return: A float value representing the estimated
    total suspended solids load reduction in tons
    produced by the given input variable values.
    """

    return product(seq) / 2000


# Protocol 2: Denitrification


def tn_2(area):
    """
    Multiply an area value (acres) by a standard coefficient.

    :param area: A float value representing the area
    of tidal marsh plantings associated with a
    shoreline management conservation practice.
    :return: A float value representing the estimated
    total nitrogen load reduction in pounds produced
    by the given area variable input.
    """

    return 85.0 * area


# Protocol 3: Sedimentation


def tp_3(area):
    """
    Multiply an area value (acres) by a standard coefficient.

    :param area: A float value representing the area
    of tidal marsh plantings associated with a
    shoreline management conservation practice.
    :return: A float value representing the estimated
    total phosphorus load reduction in pounds produced
    by the given area variable input.
    """

    return 5.289 * area


def tss_3(area):
    """
    Multiply an area value (acres) by a standard coefficient.

    :param area: A float value representing the area
    of tidal marsh plantings associated with a
    shoreline management conservation practice.
    :return: A float value representing the estimated
    total suspended solids load reduction in tons
    produced by the given area variable input.
    """

    return 3.4795 * area


# Protocol 4: Marsh Redfield Ratio


def tn_4(area):
    """
    Multiply an area value (acres) by a standard coefficient.

    :param area: A float value representing the area
    of tidal marsh plantings associated with a
    shoreline management conservation practice.
    :return: A float value representing the estimated
    total nitrogen load reduction in pounds produced
    by the given area variable input.
    """

    return 6.83 * area


def tp_4(area):
    """
    Multiply an area value (acres) by a standard coefficient.

    :param area: A float value representing the area
    of tidal marsh plantings associated with a
    shoreline management conservation practice.
    :return: A float value representing the estimated
    total phosphorus load reduction in pounds produced
    by the given area variable input.
    """

    return 0.3 * area


def reduction(data):
    """
    Extract model parameters (using defaults if necessary)
    and perform metric-specific calculations.

    :param data: A dictionary that may contain a full set of
    float values representing variables associated with the
    physical conditions affecting a shoreline management
    conservation practice.
    :return: A dictionary containing calculated model values
    for each target metric.
    """

    has_majority_design_completion = data.get('has_majority_design_completion', False)

    length_of_living_shoreline = data.get('length_of_living_shoreline', 1000.0)

    existing_avg_bank_height = data.get('existing_avg_bank_height', 4.0)

    existing_shoreline_recession_rate = data.get('existing_shoreline_recession_rate', 1.0)

    soil_bulk_density = data.get('soil_bulk_density', 93.6)

    sand_reduction_factor = data.get('sand_reduction_factor', 0.551)

    bank_instability_reduction_factor = data.get('bank_instability_reduction_factor', 1.0)

    planted_tidal_wetland_area = data.get('planted_tidal_wetland_area', 0.25)

    values = [
        length_of_living_shoreline,
        existing_avg_bank_height,
        existing_shoreline_recession_rate,
        soil_bulk_density,
        sand_reduction_factor,
        bank_instability_reduction_factor,
        planted_tidal_wetland_area,
    ]

    if not all(isinstance(x, (float, int)) for x in values):

        return {
            'tn_lbs_reduced': 0,
            'tp_lbs_reduced': 0,
            'tss_lbs_reduced': 0
        }

    if has_majority_design_completion:

        return {
            'tn_lbs_reduced_1': tn_1([
                length_of_living_shoreline,
                existing_avg_bank_height,
                existing_shoreline_recession_rate,
                soil_bulk_density,
                bank_instability_reduction_factor
            ]),
            'tn_lbs_reduced_2': tn_2(planted_tidal_wetland_area),
            'tn_lbs_reduced_4': tn_4(planted_tidal_wetland_area),
            'tp_lbs_reduced_1': tp_1([
                length_of_living_shoreline,
                existing_avg_bank_height,
                existing_shoreline_recession_rate,
                soil_bulk_density,
                bank_instability_reduction_factor
            ]),
            'tp_lbs_reduced_3': tp_3(planted_tidal_wetland_area),
            'tp_lbs_reduced_4': tp_4(planted_tidal_wetland_area),
            'tss_tons_reduced_1': tss_1([
                length_of_living_shoreline,
                existing_avg_bank_height,
                existing_shoreline_recession_rate,
                soil_bulk_density,
                sand_reduction_factor,
                bank_instability_reduction_factor
            ]),
            'tss_tons_reduced_3': tss_3(planted_tidal_wetland_area)
        }

    state_code = str(data.get('state_code', 0)).lower()

    if state_code in ['dc', 'de', 'md', 'va']:

        n_func = STATE_COEFFICIENTS.get('n').get(state_code)

        p_func = STATE_COEFFICIENTS.get('p').get(state_code)

        tss_func = STATE_COEFFICIENTS.get('tss').get(state_code)

        return {
            'tn_lbs_reduced': n_func(length_of_living_shoreline),
            'tp_lbs_reduced': p_func(length_of_living_shoreline),
            'tss_tons_reduced': tss_func(length_of_living_shoreline)
        }

    return {}
