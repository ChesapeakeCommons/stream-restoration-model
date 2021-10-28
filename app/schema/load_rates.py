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


class LoadRates(db.Model):

    __tablename__ = 'load_rates'

    __table_args__ = {
        'extend_existing': True,
    }

    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.Text)

    source = db.Column(db.Text)

    normalized_source = db.Column(db.Text)

    load_rate = db.Column(db.Numeric)

    n = db.Column(db.Numeric)

    p = db.Column(db.Numeric)

    tss = db.Column(db.Numeric)
