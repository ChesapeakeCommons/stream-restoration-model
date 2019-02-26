#!/usr/bin/env python

"""Define the InStreamHabitat schema.

Created by Viable Industries, L.L.C. on 02/05/2015.
Copyright 2016 Viable Industries, L.L.C. All rights reserved.

For license and copyright information please see the LICENSE document (the
"License") included with this software package. This file may not be used
in any manner except in compliance with the License unless required by
applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""


import math as Math


from datetime import datetime


from app import db
from app import logger


def installed_to_date(inputs, periods, percentage=False):

    planned_installation_structure_type_1 = 0
    planned_installation_structure_type_2 = 0
    planned_installation_structure_type_3 = 0
    planned_installation_structure_type_4 = 0

    planned_metrics_areas_protected = 0
    planned_metrics_areas_of_habitat_restored = 0
    planned_metrics_acres_of_wetlands_restored = 0
    planned_metrics_miles_of_living_shoreline_restored = 0
    planned_metrics_miles_of_stream_opened = 0
    planned_metrics_acres_of_oyster_habitat_restored = 0
    planned_metrics_fish_passage_improvements_number_of_passage_barriers_re = 0
    planned_metrics_fish_passage_improvements_number_of_fish_crossing_barri = 0
    planned_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou = 0
    planned_metrics_number_of_habitat_units_improved_eastern_brook_trout = 0

    installed_installation_structure_type_1 = 0
    installed_installation_structure_type_2 = 0
    installed_installation_structure_type_3 = 0
    installed_installation_structure_type_4 = 0

    installed_metrics_areas_protected = 0
    installed_metrics_areas_of_habitat_restored = 0
    installed_metrics_acres_of_wetlands_restored = 0
    installed_metrics_miles_of_living_shoreline_restored = 0
    installed_metrics_miles_of_stream_opened = 0
    installed_metrics_acres_of_oyster_habitat_restored = 0
    installed_metrics_fish_passage_improvements_number_of_passage_barriers_re = 0
    installed_metrics_fish_passage_improvements_number_of_fish_crossing_barri = 0
    installed_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou = 0
    installed_metrics_number_of_habitat_units_improved_eastern_brook_trout = 0

    for _index, _period in enumerate(periods):

        if _period.get('properties').get('measurement_period') == 'Planning':
            planned_installation_structure_type_1 += _period.get('properties').get('installation_structure_extent_1', 0) or 0
            planned_installation_structure_type_2 += _period.get('properties').get('installation_structure_extent_2', 0) or 0
            planned_installation_structure_type_3 += _period.get('properties').get('installation_structure_extent_3', 0) or 0
            planned_installation_structure_type_4 += _period.get('properties').get('installation_structure_extent_4', 0) or 0

            planned_metrics_areas_protected += _period.get('properties').get('metrics_areas_protected') if _period.get('properties').get('metrics_areas_protected') else 0
            planned_metrics_areas_of_habitat_restored += _period.get('properties').get('metrics_areas_of_habitat_restored') if _period.get('properties').get('metrics_areas_of_habitat_restored') else 0

            if _period.get('properties').get('metrics_acres_of_wetlands_restored', 0):
                planned_metrics_acres_of_wetlands_restored += _period.get('properties').get('metrics_acres_of_wetlands_restored') if _period.get('properties').get('metrics_acres_of_wetlands_restored') else 0

            planned_metrics_miles_of_living_shoreline_restored += _period.get('properties').get('metrics_miles_of_living_shoreline_restored') if _period.get('properties').get('metrics_miles_of_living_shoreline_restored') else 0
            planned_metrics_miles_of_stream_opened += _period.get('properties').get('metrics_miles_of_stream_opened') if _period.get('properties').get('metrics_miles_of_stream_opened') else 0
            planned_metrics_acres_of_oyster_habitat_restored += _period.get('properties').get('metrics_acres_of_oyster_habitat_restored') if _period.get('properties').get('metrics_acres_of_oyster_habitat_restored') else 0
            planned_metrics_fish_passage_improvements_number_of_passage_barriers_re += _period.get('properties').get('metrics_fish_passage_improvements_number_of_passage_barriers_re') if _period.get('properties').get('metrics_fish_passage_improvements_number_of_passage_barriers_re') else 0
            planned_metrics_fish_passage_improvements_number_of_fish_crossing_barri += _period.get('properties').get('metrics_fish_passage_improvements_number_of_fish_crossing_barri') if _period.get('properties').get('metrics_fish_passage_improvements_number_of_fish_crossing_barri') else 0
            planned_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou += _period.get('properties').get('metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou') if _period.get('properties').get('metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou') else 0
            planned_metrics_number_of_habitat_units_improved_eastern_brook_trout += _period.get('properties').get('metrics_number_of_habitat_units_improved_eastern_brook_trout') if _period.get('properties').get('metrics_number_of_habitat_units_improved_eastern_brook_trout') else 0

        elif _period.get('properties').get('measurement_period') == 'Installation':
            installed_installation_structure_type_1 += _period.get('properties').get('installation_structure_extent_1') if _period.get('properties').get('installation_structure_extent_1') else 0
            installed_installation_structure_type_2 += _period.get('properties').get('installation_structure_extent_2') if _period.get('properties').get('installation_structure_extent_2') else 0
            installed_installation_structure_type_3 += _period.get('properties').get('installation_structure_extent_3') if _period.get('properties').get('installation_structure_extent_3') else 0
            installed_installation_structure_type_4 += _period.get('properties').get('installation_structure_extent_4') if  _period.get('properties').get('installation_structure_extent_4') else 0

            installed_metrics_areas_protected += _period.get('properties').get('metrics_areas_protected') if _period.get('properties').get('metrics_areas_protected') else 0
            installed_metrics_areas_of_habitat_restored += _period.get('properties').get('metrics_areas_of_habitat_restored') if _period.get('properties').get('metrics_areas_of_habitat_restored') else 0

            if _period.get('properties').get('metrics_acres_of_wetlands_restored', 0):
                installed_metrics_acres_of_wetlands_restored += _period.get('properties').get('metrics_acres_of_wetlands_restored') if _period.get('properties').get('metrics_acres_of_wetlands_restored') else 0

            installed_metrics_miles_of_living_shoreline_restored += _period.get('properties').get('metrics_miles_of_living_shoreline_restored') if _period.get('properties').get('metrics_miles_of_living_shoreline_restored') else 0
            installed_metrics_miles_of_stream_opened += _period.get('properties').get('metrics_miles_of_stream_opened') if _period.get('properties').get('metrics_miles_of_stream_opened') else 0
            installed_metrics_acres_of_oyster_habitat_restored += _period.get('properties').get('metrics_acres_of_oyster_habitat_restored') if _period.get('properties').get('metrics_acres_of_oyster_habitat_restored') else 0
            installed_metrics_fish_passage_improvements_number_of_passage_barriers_re += _period.get('properties').get('metrics_fish_passage_improvements_number_of_passage_barriers_re') if _period.get('properties').get('metrics_fish_passage_improvements_number_of_passage_barriers_re') else 0
            installed_metrics_fish_passage_improvements_number_of_fish_crossing_barri += _period.get('properties').get('metrics_fish_passage_improvements_number_of_fish_crossing_barri') if _period.get('properties').get('metrics_fish_passage_improvements_number_of_fish_crossing_barri') else 0
            installed_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou += _period.get('properties').get('metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou') if _period.get('properties').get('metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou') else 0
            installed_metrics_number_of_habitat_units_improved_eastern_brook_trout += _period.get('properties').get('metrics_number_of_habitat_units_improved_eastern_brook_trout') if _period.get('properties').get('metrics_number_of_habitat_units_improved_eastern_brook_trout') else 0

    _totals = {
        'installation_structure_type_1': installed_installation_structure_type_1 or 0,
        'installation_structure_type_2': installed_installation_structure_type_2 or 0,
        'installation_structure_type_3': installed_installation_structure_type_3 or 0,
        'installation_structure_type_4': installed_installation_structure_type_4 or 0,

        'metrics_areas_protected': installed_metrics_areas_protected or 0,
        'metrics_areas_of_habitat_restored': installed_metrics_areas_of_habitat_restored or 0,
        'metrics_acres_of_wetlands_restored': installed_metrics_acres_of_wetlands_restored or 0,
        'metrics_miles_of_living_shoreline_restored': installed_metrics_miles_of_living_shoreline_restored or 0,
        'metrics_miles_of_stream_opened': installed_metrics_miles_of_stream_opened or 0,
        'metrics_acres_of_oyster_habitat_restored': installed_metrics_acres_of_oyster_habitat_restored or 0,
        'metrics_fish_passage_improvements_number_of_passage_barriers_re': installed_metrics_fish_passage_improvements_number_of_passage_barriers_re or 0,
        'metrics_fish_passage_improvements_number_of_fish_crossing_barri': installed_metrics_fish_passage_improvements_number_of_fish_crossing_barri or 0,
        'metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou': installed_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou or 0,
        'metrics_number_of_habitat_units_improved_eastern_brook_trout': installed_metrics_number_of_habitat_units_improved_eastern_brook_trout or 0
    }

    if percentage:
        _totals = {
            'installation_structure_type_1': (installed_installation_structure_type_1/planned_installation_structure_type_1)*100 if planned_installation_structure_type_1 > 0 else 0,
            'installation_structure_type_2': (installed_installation_structure_type_2/planned_installation_structure_type_2)*100 if planned_installation_structure_type_2 > 0 else 0,
            'installation_structure_type_3': (installed_installation_structure_type_3/planned_installation_structure_type_3)*100 if planned_installation_structure_type_3 > 0 else 0,
            'installation_structure_type_4': (installed_installation_structure_type_4/planned_installation_structure_type_4)*100 if planned_installation_structure_type_4 > 0 else 0,

            'metrics_areas_protected': (installed_metrics_areas_protected/planned_metrics_areas_protected)*100 if planned_metrics_areas_protected > 0 else 0,
            'metrics_areas_of_habitat_restored': (installed_metrics_areas_of_habitat_restored/planned_metrics_areas_of_habitat_restored)*100 if planned_metrics_areas_of_habitat_restored > 0 else 0,
            'metrics_acres_of_wetlands_restored': (installed_metrics_acres_of_wetlands_restored/planned_metrics_acres_of_wetlands_restored)*100 if planned_metrics_acres_of_wetlands_restored > 0 else 0,
            'metrics_miles_of_living_shoreline_restored': (installed_metrics_miles_of_living_shoreline_restored/planned_metrics_miles_of_living_shoreline_restored)*100 if planned_metrics_miles_of_living_shoreline_restored > 0 else 0,
            'metrics_miles_of_stream_opened': (installed_metrics_miles_of_stream_opened/planned_metrics_miles_of_stream_opened)*100 if planned_metrics_miles_of_stream_opened > 0 else 0,
            'metrics_fish_passage_improvements_number_of_passage_barriers_re': (installed_metrics_fish_passage_improvements_number_of_passage_barriers_re/planned_metrics_fish_passage_improvements_number_of_passage_barriers_re)*100 if planned_metrics_fish_passage_improvements_number_of_passage_barriers_re > 0 else 0,
            'metrics_fish_passage_improvements_number_of_fish_crossing_barri': (installed_metrics_fish_passage_improvements_number_of_fish_crossing_barri/planned_metrics_fish_passage_improvements_number_of_fish_crossing_barri)*100 if planned_metrics_fish_passage_improvements_number_of_fish_crossing_barri > 0 else 0,
        }

        if installed_metrics_acres_of_oyster_habitat_restored != 0 and planned_metrics_acres_of_oyster_habitat_restored != 0:
            _totals['metrics_acres_of_oyster_habitat_restored'] = (installed_metrics_acres_of_oyster_habitat_restored/planned_metrics_acres_of_oyster_habitat_restored)*100
        else:
            _totals['metrics_acres_of_oyster_habitat_restored'] = 0

        if installed_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou != 0 and planned_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou != 0:
            _totals['metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou'] = (installed_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou/planned_metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou)*100
        else:
            _totals['metrics_number_of_reintroduced_subwatersheds_eastern_brook_trou'] = 0

        if installed_metrics_number_of_habitat_units_improved_eastern_brook_trout != 0 and planned_metrics_number_of_habitat_units_improved_eastern_brook_trout != 0:
            _totals['metrics_number_of_habitat_units_improved_eastern_brook_trout'] = (installed_metrics_number_of_habitat_units_improved_eastern_brook_trout/planned_metrics_number_of_habitat_units_improved_eastern_brook_trout)*100
        else:
            _totals['metrics_number_of_habitat_units_improved_eastern_brook_trout'] = 0

    return _totals
