#!/usr/bin/env python

"""Define the User schema.

Created by Viable Industries, L.L.C. on 01/29/2015.
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

from datetime import datetime

# Import third-party dependencies

import geoalchemy2.functions as geofunc
from geoalchemy2 import Geometry
from geoalchemy2.types import Geography

# Import package dependencies

from app import db
from app import logger

from app.geometry import ST_Extent
from app.geometry import ST_GeomFromGeoJSON

from app.utilities import link_map
from app.utilities import parse_snake


class LandRiverSegment(db.Model):
    """LandRiverSegment schema definition.

    The `LandRiverSegment` database table definition.

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    __tablename__ = 'land_river_segment'
    __table_args__ = {
        'extend_existing': True,
    }

    id = db.Column(db.Integer, primary_key=True)
    
    acres = db.Column(db.Numeric)
    cbseg_92 = db.Column(db.Text)
    cbw = db.Column(db.Text)
    cntyname = db.Column(db.Text)
    dsid = db.Column(db.Integer)
    fips = db.Column(db.Text)
    fips_nhl = db.Column(db.Text)
    flow = db.Column(db.Integer)
    hgmr = db.Column(db.Text)
    lndrvrseg = db.Column(db.Text)
    majbas = db.Column(db.Text)
    majmin = db.Column(db.Text)
    major = db.Column(db.Text)
    meanprecip = db.Column(db.Text)
    minbas = db.Column(db.Text)
    minor = db.Column(db.Text)
    precip = db.Column(db.Text)
    region = db.Column(db.Text)
    rivername = db.Column(db.Text)
    riverseg = db.Column(db.Text)
    riversimu = db.Column(db.Text)
    segment_id = db.Column(db.Text, unique=True)
    st = db.Column(db.Text)
    tidalwater = db.Column(db.Text)
    uniqid = db.Column(db.Integer)
    watershed = db.Column(db.Text)

    geometry = db.Column(Geography(**{
        'geometry_type': 'GEOMETRY',
        'srid': 4326
    }))

    #: Specify fields that should be available to keyword searches

    search_fields = [
        'name'
    ]

    #: Expose a subset of model column attributes

    @classmethod
    def column_subset(cls, exclude=None):

        if exclude:

            if isinstance(exclude, list):

                return [
                    key for key in cls.__table__.columns.keys()
                    if key not in exclude
                ]

            elif isinstance(exclude, basestring):

                return [
                    key for key in cls.__table__.columns.keys()
                    if key not in exclude.split(',')
                ]

        return cls.__table__.columns.keys()


    def search_result(self):

        return {
            'id': self.id,
            'category': 'geography',
            'name': self.name,
            'subcategory': self.get_category()
        }


    # def build_links(self):

    #     return {
    #         'organization': link_map(
    #             collection='organizations',
    #             feature_id=self.organization_id
    #         ),
    #         'program': link_map(
    #             collection='programs',
    #             feature_id=self.program_id
    #         ),
    #         'self': link_map(
    #             collection='geographies',
    #             feature_id=self.id
    #         )
    #     }
