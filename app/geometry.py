#!/usr/bin/env python

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
