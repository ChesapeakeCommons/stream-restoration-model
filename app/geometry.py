#!/usr/bin/env python

"""Define the FieldDoc Endpoint Class.

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

# Import third-party dependencies

from geoalchemy2 import Geometry
from geoalchemy2.functions import GenericFunction


class ST_GeomFromGeoJSON(GenericFunction):
    name = 'ST_GeomFromGeoJSON'
    type = Geometry

class ST_GeomFromText(GenericFunction):
    name = 'ST_GeomFromText'
    type = Geometry

class ST_MakeValid(GenericFunction):
    name = 'ST_MakeValid'
    type = Geometry

class ST_Transform(GenericFunction):
    name = 'ST_Transform'
    type = Geometry

class ST_AsGeoJSON(GenericFunction):
    name = 'ST_AsGeoJSON'
    type = Geometry

class ST_SetSRID(GenericFunction):
    name = 'ST_SetSRID'
    type = Geometry

class ST_Extent(GenericFunction):
    name = 'ST_Extent'
    type = Geometry

class ST_MakeEnvelope(GenericFunction):
    name = 'ST_MakeEnvelope'
    type = Geometry
