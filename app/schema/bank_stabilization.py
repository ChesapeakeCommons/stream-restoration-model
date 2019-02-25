#!/usr/bin/env python

"""Define the BMPBankStabilization schema.

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


import math


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


class BMPBankStabilization(db.Model):
    """BMPBankStabilization schema definition.

    The `BMPBankStabilization` database table definition.

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    __tablename__ = 'bmp_bank_stabilization'
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

    installation_length_of_streambank = db.Column(db.Float(8), default=0.0)
    installation_eroding_bank_height = db.Column(db.Float(8), default=0.0)
    installation_eroding_bank_horizontal_width = db.Column(db.Float(8), default=0.0)
    installation_ler_evaluation_basis = db.Column(db.String, default="")
    installation_lateral_erosion_rate = db.Column(db.Float(8), default=0.0)
    installation_soil_bulk_density = db.Column(db.Float(8), default=0.0)
    installation_soil_n_content = db.Column(db.Float(8), default=0.0)
    installation_soil_p_content = db.Column(db.Float(8), default=0.0)

    monitoring_design_criteria_1 = db.Column(db.Boolean, default=False)
    monitoring_design_criteria_2 = db.Column(db.Boolean, default=False)
    monitoring_design_criteria_3 = db.Column(db.Boolean, default=False)
    monitoring_hydraulic = db.Column(db.Boolean, default=False)
    monitoring_geomorphic_1 = db.Column(db.Boolean, default=False)
    monitoring_geomorphic_2 = db.Column(db.Boolean, default=False)
    monitoring_geomorphic_3 = db.Column(db.Boolean, default=False)
    monitoring_geomorphic_4 = db.Column(db.Boolean, default=False)

    metrics_bank_erosion_hazard_index_rating = db.Column(db.Float(8), default=0.0)
    metrics_near_bank_stress_rating = db.Column(db.Float(8), default=0.0)
    metrics_riffle_stability_index = db.Column(db.Float(8), default=0.0)
    metrics_logarithm_of_relative_bed_stability = db.Column(db.Float(8), default=0.0)
    metrics_substrate_mean_particle_size = db.Column(db.Float(8), default=0.0)
    metrics_streambed_percent_fines = db.Column(db.Float(8), default=0.0)


    def reduction(self, value, preinstallation=False):

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
        installation_lateral_erosion_rate = value.get('installation_lateral_erosion_rate', 0) if value.get('installation_lateral_erosion_rate', 0) else 0
        installation_length_of_streambank = value.get('installation_length_of_streambank', 0) if value.get('installation_length_of_streambank', 0) else 0
        installation_soil_bulk_density = value.get('installation_soil_bulk_density', 0) if value.get('installation_soil_bulk_density', 0) else 0

        ler = installation_lateral_erosion_rate * 0.5

        if preinstallation:
            ler = installation_lateral_erosion_rate

        base_length = installation_length_of_streambank
        soil_density = installation_soil_bulk_density

        installation_eroding_bank_height = value.get('installation_eroding_bank_height', 0) if value.get('installation_eroding_bank_height', 0) else 0
        installation_eroding_bank_horizontal_width = value.get('installation_eroding_bank_horizontal_width', 0) if value.get('installation_eroding_bank_horizontal_width', 0) else 0

        square_root = math.sqrt((installation_eroding_bank_height * installation_eroding_bank_height) + (installation_eroding_bank_horizontal_width * installation_eroding_bank_horizontal_width))
        load_total = base_length * square_root * ler * soil_density

        installation_soil_n_content = value.get('installation_soil_n_content', 0) if value.get('installation_soil_n_content', 0) else 0
        installation_soil_p_content = value.get('installation_soil_p_content', 0) if value.get('installation_soil_p_content', 0) else 0

        return {
            'nitrogen': ((load_total)/2000)*installation_soil_n_content,
            'phosphorus': ((load_total)/2000)*installation_soil_p_content,
            'sediment': (load_total)/2000
        }


    def miles_of_streambank_restored(self, value):

        installation_length_of_streambank = value.get('installation_length_of_streambank', 0) if value.get('installation_length_of_streambank', 0) else 0

        return (installation_length_of_streambank / 5280)
