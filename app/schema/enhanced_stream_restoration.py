#!/usr/bin/env python

"""Define the EnhancedStreamRestoration schema.

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

from app.schema.project import Project
from app.schema.site import Site
from app.schema.practice import Practice
from app.schema.urban_ual_state_load_reductions import UrbanStateUAL
from app.schema.nutrient import Nutrient

from flask.ext.restless.helpers import to_dict
from flask.ext.restless.helpers import get_relations


class EnhancedStreamRestoration(db.Model):
    """EnhancedStreamRestoration schema definition.

    The `EnhancedStreamRestoration` database table definition.

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    __tablename__ = 'enhanced_stream_restoration'
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, primary_key=True)
    measurement_period = db.Column(db.String, default="")
    report_date = db.Column(db.Date, default=datetime.utcnow())
    existing_riparian_landuse = db.Column(db.String, default="")
    upland_landuse = db.Column(db.String, default="")
    wip_reporting_agency = db.Column(db.String, default="")
    notes = db.Column(db.String, default="")

    adaptive_management_hydrologic = db.Column(db.Boolean, default=False)
    adaptive_management_hydraulic = db.Column(db.Boolean, default=False)
    adaptive_management_riparian_vegetation = db.Column(db.Boolean, default=False)
    bulk_density_of_soil_in_hyporheic_zone = db.Column(db.Float(8), default=0.0)
    connected_floodplain_surface_area = db.Column(db.Float(8), default=0.0)
    floodplain_connection_volume = db.Column(db.Float(8), default=0.0)
    fraction_of_annual_runoff_treated_by_floodplain = db.Column(db.Float(8), default=0.0)
    left_bank_bankfull_height = db.Column(db.Float(8), default=0.0)
    left_bank_riparian_vegetative_zone_width = db.Column(db.Float(8), default=0.0)
    left_bank_vegetative_protection = db.Column(db.Float(8), default=0.0)
    length_of_left_bank_with_improved_connectivity = db.Column(db.Float(8), default=0.0)
    length_of_right_bank_with_improved_connectivity = db.Column(db.Float(8), default=0.0)
    mean_annual_bankfull_flow = db.Column(db.Float(8), default=0.0)
    monthly_flow_frequency_probability_plot = db.Column(db.Float(8), default=0.0)
    number_of_overbank_flows_per_year = db.Column(db.Float(8), default=0.0)
    project_left_bank_height = db.Column(db.Float(8), default=0.0)
    project_right_bank_height = db.Column(db.Float(8), default=0.0)
    rainfall_depth_where_connection_occurs = db.Column(db.Float(8), default=0.0)
    right_bank_bankfull_height = db.Column(db.Float(8), default=0.0)
    right_bank_riparian_vegetative_zone_width = db.Column(db.Float(8), default=0.0)
    right_bank_vegetative_protection = db.Column(db.Float(8), default=0.0)
    stream_length_reconnected_at_floodplain = db.Column(db.Float(8), default=0.0)
    stream_width_at_bankfull = db.Column(db.Float(8), default=0.0)
    stream_width_at_mean_base_flow = db.Column(db.Float(8), default=0.0)
    watershed_contributing_area = db.Column(db.Float(8), default=0.0)
    watershed_impervious_area = db.Column(db.Float(8), default=0.0)
    watershed_pervious_area = db.Column(db.Float(8), default=0.0)

    has_majority_design_completion = db.Column(db.Boolean, default=None)

    override_linear_feet_in_coastal_plain = db.Column(db.Float(8), default=0.0)
    override_linear_feet_in_noncoastal_plain = db.Column(db.Float(8), default=0.0)
    override_linear_feet_in_total = db.Column(db.Float(8), default=0.0)


    def efficiency(self):
        return {
            "n_eff": 0.2,
            "p_eff": 0.3,
            "s_eff": 0.2
        }

    def reduction(self, value, readings, load_data, has_majority_design_completion):

        """If the measurement_period is Pre-Installation the LER will use the
        raw installation_lateral_erosion_rate provided by the user.

        If the measurement_period is Planning or Installation the LER will be
        halved (i.e., multipled by 0.5).

        The Expert Panel (EP) guidance specifies a default value of 50%,
        subject to post-installation monitoring which could justify a larger
        reduction efficiency.[1]

        [1] Gene Yagow, Senior Research Scientist, Biological Systems
            Engineering Department Virginia Tech
        """
        if has_majority_design_completion:
            return {
                'nitrogen': {
                    'protocol_2': self.nitrogen_protocol_2(value, load_data),
                    'protocol_3': self.nitrogen_protocol_3(readings, load_data)
                },
                'phosphorus': {
                    'protocol_3': self.phosphorus_protocol_3(readings, load_data)
                },
                'sediment': self.sediment_protocol_1(readings, load_data)
            }
        else:
            return {
                'nitrogen': {
                    'protocol_2': 0,
                    'protocol_3': 0
                },
                'phosphorus': {
                    'protocol_3': 0
                },
                'sediment': 0,
                'overrides': {
                    'nitrogen': {
                        'protocol_2': self.nitrogen(value),
                        'protocol_3': 0
                    },
                    'phosphorus': {
                        'protocol_3': self.phosphorus(value)
                    },
                    'sediment': self.sediment(value)
                }
            }


    def bank_height_ratio(self, bank_height, bankfull_height):

        behi = 0

        if bank_height:

            behi = (bank_height / bankfull_height)

        return behi


    def fraction_of_runoff_treated_by_floodplain(self, fraction_in_channel, fraction_runoff_treated):

        fraction = 0

        if fraction_in_channel and fraction_runoff_treated:
            fraction = (Math.pow(fraction_in_channel, 2)+0.3*fraction_in_channel-0.98)*Math.pow(fraction_runoff_treated,2)+(-2.35*fraction_in_channel+2)*fraction_runoff_treated

        return fraction


    def nitrogen_protocol_2(self, value, loaddata):

        project_left_bank_height = value.get("project_left_bank_height", 0) if value.get("project_left_bank_height", 0) else 0
        left_bank_bankfull_height = value.get("left_bank_bankfull_height", 0) if value.get("left_bank_bankfull_height", 0) else 0

        project_right_bank_height = value.get("project_right_bank_height", 0) if value.get("project_right_bank_height", 0) else 0
        right_bank_bankfull_height = value.get("right_bank_bankfull_height", 0) if value.get("right_bank_bankfull_height", 0) else 0

        bulk_density = 125
        nitrogen = 0
        left_behi = self.bank_height_ratio(project_left_bank_height, left_bank_bankfull_height)
        right_behi = self.bank_height_ratio(project_right_bank_height, right_bank_bankfull_height)
        left_bank = 0
        right_bank = 0
        year = 365
        coefficient = 0.000195

        """NOVEMBER 2017 MDNR UPDATES

        1. CHANGE CO-EFFICIENT FROM 0.000195 to 0.075
        2. Change the BEHI+

        """

        length_of_left_bank_with_improved_connectivity = value.get("length_of_left_bank_with_improved_connectivity", 0) if value.get("length_of_left_bank_with_improved_connectivity", 0) else 0
        length_of_right_bank_with_improved_connectivity = value.get("length_of_right_bank_with_improved_connectivity", 0) if value.get("length_of_right_bank_with_improved_connectivity", 0) else 0
        stream_width_at_mean_base_flow = value.get("stream_width_at_mean_base_flow", 0) if value.get("stream_width_at_mean_base_flow", 0) else 0

        if left_behi < 1.1:

            left_bank = length_of_left_bank_with_improved_connectivity * (stream_width_at_mean_base_flow / 2 + 5)

        if right_behi < 1.1:

            right_bank = length_of_right_bank_with_improved_connectivity * (stream_width_at_mean_base_flow / 2 + 5)

        nitrogen = ((left_bank + right_bank) * 5 * bulk_density / 2000) * coefficient * year

        return nitrogen


    def nitrogen_protocol_3(self, readings, loaddata):

        nitrogen = 0
        preProjectData = None
        planningData = None
        efficiency = self.efficiency()['n_eff']

        """ Before we move on we need to make sure we have the appropriate
            pre-project data which impacts the rest of the calculation
        """
        for _reading in readings:
            if _reading and _reading.get('properties') and _reading.get('properties').get('measurement_period') == 'Pre-Project' and _reading.get('properties').get('has_majority_design_completion'):
                preProjectData = _reading.get('properties')
            elif _reading and _reading.get('properties') and _reading.get('properties').get('measurement_period') == 'Planning' and _reading.get('properties').get('has_majority_design_completion'):
                planningData = _reading.get('properties')

        if preProjectData and planningData:
            plannedRunoffFraction = self.fraction_of_runoff_treated_by_floodplain(planningData.get('rainfall_depth_where_connection_occurs', 0), planningData.get('floodplain_connection_volume', 0))
            preprojectRunoffFraction = self.fraction_of_runoff_treated_by_floodplain(preProjectData.get('rainfall_depth_where_connection_occurs', 0), preProjectData.get('floodplain_connection_volume', 0))

            watershed_impervious_area = 0
            if planningData.get('watershed_impervious_area'):
                watershed_impervious_area = planningData.get('watershed_impervious_area')

            nitrogen = 0

            if loaddata and 'impervious' in loaddata and 'pervious' in loaddata and 'tn_ual' in loaddata['impervious'] and 'tn_ual' in loaddata['pervious']:
                nitrogen = (plannedRunoffFraction-preprojectRunoffFraction)*efficiency*(watershed_impervious_area*loaddata['impervious']['tn_ual']+watershed_impervious_area*loaddata['pervious']['tn_ual'])

        return nitrogen;


    def phosphorus_protocol_3(self, readings, loaddata):

        phosphorus = 0
        preProjectData = None
        planningData = None
        efficiency = self.efficiency()['p_eff']

        """ Before we move on we need to make sure we have the appropriate
            pre-project data which impacts the rest of the calculation
        """
        for _reading in readings:
            if _reading and _reading.get('properties') and _reading.get('properties').get('measurement_period') == 'Pre-Project' and _reading.get('properties').get('has_majority_design_completion'):
                preProjectData = _reading.get('properties')
            elif _reading and _reading.get('properties') and _reading.get('properties').get('measurement_period') == 'Planning' and _reading.get('properties').get('has_majority_design_completion'):
                planningData = _reading.get('properties')

        if preProjectData and planningData:
            plannedRunoffFraction = self.fraction_of_runoff_treated_by_floodplain(planningData.get('rainfall_depth_where_connection_occurs', 0), planningData.get('floodplain_connection_volume', 0))
            preprojectRunoffFraction = self.fraction_of_runoff_treated_by_floodplain(preProjectData.get('rainfall_depth_where_connection_occurs', 0), preProjectData.get('floodplain_connection_volume', 0))

            watershed_impervious_area = 0
            if planningData.get('watershed_impervious_area'):
                watershed_impervious_area = planningData.get('watershed_impervious_area')

            phosphorus = 0

            if loaddata and 'impervious' in loaddata and 'pervious' in loaddata and 'tp_ual' in loaddata['impervious'] and 'tp_ual' in loaddata['pervious']:
                phosphorus = (plannedRunoffFraction-preprojectRunoffFraction)*efficiency*(watershed_impervious_area*loaddata['impervious']['tp_ual']+watershed_impervious_area*loaddata['pervious']['tp_ual'])

        return phosphorus


    def sediment_protocol_1(self, readings, loaddata):

        sediment = 0
        preProjectData = None
        planningData = None
        efficiency = self.efficiency()['s_eff']

        """ Before we move on we need to make sure we have the appropriate
            pre-project data which impacts the rest of the calculation
        """
        for _reading in readings:

            if _reading and _reading.get('properties') and _reading.get('properties').get('measurement_period') == 'Pre-Project' and _reading.get('properties').get('has_majority_design_completion'):
                preProjectData = _reading.get('properties')
            elif _reading and _reading.get('properties') and _reading.get('properties').get('measurement_period') == 'Planning' and _reading.get('properties').get('has_majority_design_completion'):
                planningData = _reading.get('properties')

        if preProjectData and planningData:

            plannedRunoffFraction = self.fraction_of_runoff_treated_by_floodplain(planningData.get('rainfall_depth_where_connection_occurs', 0), planningData.get('floodplain_connection_volume', 0))
            preprojectRunoffFraction = self.fraction_of_runoff_treated_by_floodplain(preProjectData.get('rainfall_depth_where_connection_occurs', 0), preProjectData.get('floodplain_connection_volume', 0))

            watershed_impervious_area = 0

            if planningData.get('watershed_impervious_area'):
                
                watershed_impervious_area = planningData.get('watershed_impervious_area')

            sediment = 0

            if loaddata and 'impervious' in loaddata and 'pervious' in loaddata and 'tss_ual' in loaddata['impervious'] and 'tss_ual' in loaddata['pervious']:
                sediment = (plannedRunoffFraction-preprojectRunoffFraction)*efficiency*(watershed_impervious_area*loaddata['impervious']['tss_ual']+watershed_impervious_area*loaddata['pervious']['tss_ual'])

        return sediment


    def nitrogen(self, value):

        coastal_ = 0
        noncoastal_ = 0

        if value.get('override_linear_feet_in_coastal_plain', 0):

            coastal_ = value.get('override_linear_feet_in_coastal_plain', 0) * 0.075

        if value.get('override_linear_feet_in_noncoastal_plain', 0):

            noncoastal_ = value.get('override_linear_feet_in_noncoastal_plain', 0) * 0.075

        return (coastal_+noncoastal_)


    def phosphorus(self, value):

        coastal_ = 0
        noncoastal_ = 0

        if value.get('override_linear_feet_in_coastal_plain', 0):

            coastal_ = value.get('override_linear_feet_in_coastal_plain', 0) * 0.068

        if value.get('override_linear_feet_in_noncoastal_plain', 0):

            noncoastal_ = value.get('override_linear_feet_in_noncoastal_plain', 0) * 0.068

        return (coastal_+noncoastal_)


    def sediment(self, value):

        coastal_ = 0
        noncoastal_ = 0

        if value.get('override_linear_feet_in_coastal_plain'):

            coastal_ = value.get('override_linear_feet_in_coastal_plain') * 15.13

        if value.get('override_linear_feet_in_noncoastal_plain'):

            noncoastal_ = value.get('override_linear_feet_in_noncoastal_plain') * 44.88

        return ((coastal_ + noncoastal_) / 2000)


    def miles_of_streambank_restored(self, value):

        miles = 0

        if not value.get('has_majority_design_completion'):

            coastal_ = 0
            noncoastal_ = 0

            if value.get('override_linear_feet_in_coastal_plain', 0):

                coastal_ = value.get('override_linear_feet_in_coastal_plain', 0)

            if value.get('override_linear_feet_in_noncoastal_plain', 0):

                noncoastal_ = value.get('override_linear_feet_in_noncoastal_plain', 0)

            miles = ((coastal_ + noncoastal_) / 5280)

            return miles

        project_left_bank_height = value.get("project_left_bank_height") or 0
        left_bank_bankfull_height = value.get("left_bank_bankfull_height") or 0

        project_right_bank_height = value.get("project_right_bank_height") or 0
        right_bank_bankfull_height = value.get("right_bank_bankfull_height") or 0

        length_of_left_bank_with_improved_connectivity = value.get("length_of_left_bank_with_improved_connectivity") or 0
        length_of_right_bank_with_improved_connectivity = value.get("length_of_right_bank_with_improved_connectivity") or 0

        stream_width_at_mean_base_flow = value.get("stream_width_at_mean_base_flow") or 0
        stream_length_reconnected_at_floodplain = value.get("stream_length_reconnected_at_floodplain") or 0

        left_behi = self.bank_height_ratio(project_left_bank_height, left_bank_bankfull_height)
        right_behi = self.bank_height_ratio(project_right_bank_height, right_bank_bankfull_height)
        left_bank = 0
        right_bank = 0
        feet_to_miles = 5280

        if left_behi < 1.1:

            left_bank = length_of_left_bank_with_improved_connectivity

        if right_behi < 1.1:

            right_bank = length_of_right_bank_with_improved_connectivity

        miles = ((left_bank + right_bank + stream_length_reconnected_at_floodplain) / feet_to_miles)

        return miles


    def acres_of_streambank_restored(self, value):

        project_left_bank_height = value.get("project_left_bank_height") or 0
        left_bank_bankfull_height = value.get("left_bank_bankfull_height") or 0

        project_right_bank_height = value.get("project_right_bank_height") or 0
        right_bank_bankfull_height = value.get("right_bank_bankfull_height") or 0

        length_of_left_bank_with_improved_connectivity = value.get("length_of_left_bank_with_improved_connectivity") or 0
        length_of_right_bank_with_improved_connectivity = value.get("length_of_right_bank_with_improved_connectivity") or 0

        stream_width_at_mean_base_flow = value.get("stream_width_at_mean_base_flow") or 0
        stream_length_reconnected_at_floodplain = value.get("stream_length_reconnected_at_floodplain") or 0

        acres = 0
        left_behi = self.bank_height_ratio(project_left_bank_height, left_bank_bankfull_height)
        right_behi = self.bank_height_ratio(project_right_bank_height, right_bank_bankfull_height)
        left_bank = 0
        right_bank = 0
        to_acres = 43560

        if left_behi < 1.1:

            left_bank = length_of_left_bank_with_improved_connectivity

        if right_behi < 1.1:

            right_bank = length_of_right_bank_with_improved_connectivity

        acres = (((left_bank * (stream_width_at_mean_base_flow / 2 + 5)) + (right_bank * (stream_width_at_mean_base_flow / 2 + 5)) + stream_length_reconnected_at_floodplain) / to_acres)

        return acres


    def acres_of_floodplain_reconnected(self, value):

        acres = value.get("connected_floodplain_surface_area", 0)

        return acres
