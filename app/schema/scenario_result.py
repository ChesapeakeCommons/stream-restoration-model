#!/usr/bin/env python

"""Define the User schema.

Created by Viable Industries, L.L.C. on 12/27/2015.
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

# Import standard dependencies

import json

# Import package dependencies

from app import db
from app import logger
from app import serializer

from app.utilities import parse_snake


class ScenarioResult(db.Model):
    """ScenarioResult schema definition.

    The `ScenarioResult` database table definition

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    __tablename__ = 'scenario_result'
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, primary_key=True)
    
    bmp_full_name = db.Column(db.Text)
    bmp_short_name = db.Column(db.Text)
    bmp_unit_full_name = db.Column(db.Text)
    geography_full_name = db.Column(db.Text)
    land_river_segment = db.Column(db.Text)
    sector = db.Column(db.Text)
    tn_lbs_reduced_per_unit = db.Column(db.Numeric)
    tp_lbs_reduced_per_unit = db.Column(db.Numeric)
    tss_lbs_reduced_per_unit = db.Column(db.Numeric)

    # `Organization` relation to associate with this feature.

    practice_id = db.Column(
        db.Integer,
        db.ForeignKey('practice.id'))

    practice = db.relationship('Practice', **{
        'uselist': False,
        'foreign_keys': 'ScenarioResult.practice_id'
    })

    # `Program` relation to associate with this feature.

    segment_id = db.Column(
        db.Integer,
        db.ForeignKey('land_river_segment.id'))

    segment = db.relationship('LandRiverSegment', **{
        'uselist': False,
        'foreign_keys': 'ScenarioResult.segment_id'
    })
