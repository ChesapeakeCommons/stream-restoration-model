#!/usr/bin/env python

"""Define the BMPStormwater schema.

Created by Viable Industries, L.L.C. on 02/05/2017.
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
from app.schema.loaddata import LoadData
from app.schema.efficiency import Efficiency
from app.schema.urban_ual_state_load_reductions import UrbanStateUAL
from app.schema.nutrient import Nutrient


from flask.ext.restless.helpers import to_dict
from flask.ext.restless.helpers import get_relations


class BMPStormwater(db.Model):
    """BMPStormwater schema definition.

    The `BMPStormwater` database table definition.

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    __tablename__ = 'bmp_stormwater'
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

    practice_1_name = db.Column(db.Text, default="")
    practice_1_extent = db.Column(db.Float(8), default=0.0)

    practice_2_name = db.Column(db.Text, default="")
    practice_2_extent = db.Column(db.Float(8), default=0.0)

    practice_3_name = db.Column(db.Text, default="")
    practice_3_extent = db.Column(db.Float(8), default=0.0)

    practice_4_name = db.Column(db.Text, default="")
    practice_4_extent = db.Column(db.Float(8), default=0.0)

    project_type = db.Column(db.Text, default="")
    site_reduction_classification = db.Column(db.Text, default="")

    impervious_area = db.Column(db.Float(8), default=0.0)
    total_drainage_area = db.Column(db.Float(8), default=0.0)
    runoff_volume_captured = db.Column(db.Float(8), default=0.0)

    """Monitoring."""
    monitoring_bird_count = db.Column(db.Float(8), default=0.0)
    monitoring_small_animal_count = db.Column(db.Float(8), default=0.0)

    monitoring_check_1 = db.Column(db.Boolean, default=False)
    monitoring_check_2 = db.Column(db.Boolean, default=False)
    monitoring_check_3 = db.Column(db.Boolean, default=False)
    monitoring_check_4 = db.Column(db.Boolean, default=False)
    monitoring_check_5 = db.Column(db.Boolean, default=False)

    """Timestamps."""
    created_on = db.Column(db.DateTime)
    modified_on = db.Column(db.DateTime)

    custom_nutrient_reductions_id = db.Column(db.Integer, db.ForeignKey('nutrient.id'))
    custom_nutrient_reductions = db.relationship('Nutrient', **{
        'foreign_keys': 'BMPStormwater.custom_nutrient_reductions_id',
        'uselist': False,
        'backref': db.backref('nutrients_stormwater')
    })

    """Practice to associate with this report."""
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id', ondelete='CASCADE'))
    practice = db.relationship('Practice', **{
      'primaryjoin': 'or_(BMPStormwater.practice_id==Practice.id)',
      'backref': db.backref('readings_stormwater', cascade='delete, delete-orphan'),
      'uselist': False
    })

    """Organization Account to associate with this report."""
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('Account', **{
      'foreign_keys': 'BMPStormwater.account_id',
      'uselist': False
    })

    """User account that originally created the Site."""
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship("User", **{
        'foreign_keys': 'BMPStormwater.creator_id',
        'uselist': False
    })

    """User account that last edited this Site."""
    last_modified_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_modified_by = db.relationship('User', **{
        'foreign_keys': 'BMPStormwater.last_modified_by_id',
        'uselist': False
    })

    def get_practice_data(self, practice_id):
        """Process the remaining practice information and add it to
        our list of practices for this site.
        """
        _practice = Practice.query.get(practice_id)
        _relations = frozenset(get_relations(Practice))
        _deep = dict((r, {}) for r in _relations)
        _thisPractice = to_dict(_practice, _deep, session=db.session)

        """Prepare the Site information to be served as JSON."""
        _site = _practice.site
        _relations = frozenset(get_relations(Site))
        _deep = dict((r, {}) for r in _relations)
        _thisSite = to_dict(_site, _deep, session=db.session)

        """Prepare the Site information to be served as JSON."""
        _project = _practice.site.project
        _relations = frozenset(get_relations(Project))
        _deep = dict((r, {}) for r in _relations)
        _thisProject = to_dict(_project, _deep, session=db.session)

        """With the Site information loaded, we need to grab the UrbanStateUAL
        for this practice as well. Prepare the UrbanStateUAL information to be
        served as JSON.
        """
        _urbanStateUAL = UrbanStateUAL.query.filter(UrbanStateUAL.state == _thisSite.get('properties').get('state')).all()

        _load_data = {
            "impervious": {
                "tss_ual": 0,
                "tn_ual": 0,
                "tp_ual": 0
            },
            "pervious": {
                "tss_ual": 0,
                "tn_ual": 0,
                "tp_ual": 0
            }
        }

        for _load in _urbanStateUAL:
            _relations = frozenset(get_relations(UrbanStateUAL))
            _deep = dict((r, {}) for r in _relations)
            _thisLoad = to_dict(_load, _deep, session=db.session)

            if _thisLoad.get('properties').get('developed_type') == 'impervious':
                _load_data['impervious']['tss_ual'] = _thisLoad.get('properties').get('tss_ual')
                _load_data['impervious']['tn_ual'] = _thisLoad.get('properties').get('tn_ual')
                _load_data['impervious']['tp_ual'] = _thisLoad.get('properties').get('tp_ual')
            elif _thisLoad.get('properties').get('developed_type') == 'pervious':
                _load_data['pervious']['tss_ual'] = _thisLoad.get('properties').get('tss_ual')
                _load_data['pervious']['tn_ual'] = _thisLoad.get('properties').get('tn_ual')
                _load_data['pervious']['tp_ual'] = _thisLoad.get('properties').get('tp_ual')

        return {
            "practice": _thisPractice,
            "load_data": _load_data,
            "site": _thisSite,
            "project": _thisProject
        }

    def get_summary(self, practice_id):

        _summary = self.get_practice_data(practice_id)

        """Loop over each practice measurement_period and build a 'Report'
        object."""
        _practice = _summary.get('practice').get('properties')
        _periods = _practice.get('readings_stormwater')

        _has_planning_data = False
        _has_installation_data = False
        _has_monitoring_data = False

        _defaults = None

        if len(_periods):
            for _index, _period in enumerate(_periods):
                _this = _period.get('properties')

                """Get any custom nutrients for all the measurement periods."""
                if 'custom_nutrient_reductions_id' in _this and\
                   _this.get('custom_nutrient_reductions_id'):
                    custom_nutrient_id_ = _this.get('custom_nutrient_reductions_id')
                    custom_nutrients_ = Nutrient.query.get(custom_nutrient_id_)
                    _period['properties']['custom_nutrient_reductions'] = {
                        "id": custom_nutrients_.id,
                        "nitrogen": custom_nutrients_.nitrogen,
                        "phosphorus": custom_nutrients_.phosphorus,
                        "sediment": custom_nutrients_.sediment
                    }
                else:
                    _period['properties']['custom_nutrient_reductions'] = None

                if _this.get('measurement_period') == 'Planning':

                    _period['properties']['preinstallation'] = self.reduction(_this, _summary.get('load_data', None), True)
                    _period['properties']['planning'] = self.reduction(_this, _summary.get('load_data', None))

                    _has_planning_data = True

                    _defaults = _period

                elif _this.get('measurement_period') == 'Installation':

                    _period['properties']['installation'] = self.reduction(_this, _summary.get('load_data', None))

                    _has_installation_data = True

                elif _this.get('measurement_period') == 'Monitoring':

                    _has_monitoring_data = True

                if _this.get('measurement_period') == 'Planning' or _this.get('measurement_period') == 'Installation':
                    """Metrics are the same regardless of measurement_period."""
                    _period['properties']['metrics'] = {
                        'gallons_per_year_of_stormwater_detained_or_infiltrated': self.gallons_per_year_of_stormwater_detained_or_infiltrated(_this),
                        'acres_of_protected_bmps_to_reduce_stormwater_runoff': self.acres_of_protected_bmps_to_reduce_stormwater_runoff(_this),
                        'acres_of_installed_bmps_to_reduce_stormwater_runoff': self.acres_of_installed_bmps_to_reduce_stormwater_runoff(_this)
                    }

        """How much of the practice has been installed to date?"""
        _practice['quantity_installed'] = self.installed_to_date(_periods)
        _practice['percentage_installed'] = self.installed_to_date(_periods, True)

        _practice['has_planning_data'] = _has_planning_data
        _practice['has_installation_data'] = _has_installation_data
        _practice['has_monitoring_data'] = _has_monitoring_data

        _practice['defaults'] = _defaults

        """Remove County and Segment boundary prior to display."""
        if 'site' in _summary and \
           'properties' in _summary['site'] and \
           'county' in _summary['site']['properties'] and \
           _summary['site']['properties']['county'] and \
           'geometry' in _summary['site']['properties']['county']:
           _summary['site']['properties']['county']['geometry'] = None

        if 'site' in _summary and \
           'properties' in _summary['site'] and \
           'segment' in _summary['site']['properties'] and \
           _summary['site']['properties']['segment'] and \
           'geometry' in _summary['site']['properties']['segment']:
           _summary['site']['properties']['segment']['geometry'] = None

        """Remove User Data prior to display."""
        del _summary['site']['properties']['last_modified_by']
        del _summary['site']['properties']['created_by']

        return {
            "site": _summary.get('site'),
            "practice": _summary.get('practice')
        }

    def reduction(self, value, load_data, preinstallation=False):

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
        return {
            'nitrogen': self.nitrogen(value, load_data, preinstallation=preinstallation),
            'phosphorus': self.phosphorus(value, load_data, preinstallation=preinstallation),
            'sediment': self.sediment(value, load_data, preinstallation=preinstallation)
        }

    def installed_to_date(self, periods, percentage=False):

        planned_total_nitrogen = 0
        planned_total_phosphorus = 0
        planned_total_sediment = 0
        planned_gallons_per_year_of_stormwater_detained_or_infiltrated = 0
        planned_acres_of_protected_bmps_to_reduce_stormwater_runoff = 0
        planned_acres_of_installed_bmps_to_reduce_stormwater_runoff = 0
        planned_practice_1_extent = 0
        planned_practice_2_extent = 0
        planned_practice_3_extent = 0
        planned_practice_4_extent = 0
        planned_impervious_area = 0
        planned_total_drainage_area = 0

        installed_total_nitrogen = 0
        installed_total_phosphorus = 0
        installed_total_sediment = 0
        installed_gallons_per_year_of_stormwater_detained_or_infiltrated = 0
        installed_acres_of_protected_bmps_to_reduce_stormwater_runoff = 0
        installed_acres_of_installed_bmps_to_reduce_stormwater_runoff = 0
        installed_practice_1_extent = 0
        installed_practice_2_extent = 0
        installed_practice_3_extent = 0
        installed_practice_4_extent = 0
        installed_impervious_area = 0
        installed_total_drainage_area = 0

        for _index, _period in enumerate(periods):

            if _period.get('properties').get('measurement_period') == 'Planning':
                planned_total_nitrogen += _period.get('properties').get('planning').get('nitrogen', 0).get('value', 0)
                planned_total_phosphorus += _period.get('properties').get('planning').get('phosphorus', 0).get('value', 0)
                planned_total_sediment += _period.get('properties').get('planning').get('sediment', 0).get('value', 0)
                planned_gallons_per_year_of_stormwater_detained_or_infiltrated += _period.get('properties').get('metrics').get('gallons_per_year_of_stormwater_detained_or_infiltrated', 0)
                planned_acres_of_protected_bmps_to_reduce_stormwater_runoff += _period.get('properties').get('metrics').get('acres_of_protected_bmps_to_reduce_stormwater_runoff', 0)
                planned_acres_of_installed_bmps_to_reduce_stormwater_runoff += _period.get('properties').get('metrics').get('acres_of_installed_bmps_to_reduce_stormwater_runoff', 0)

                planned_practice_1_extent = _period.get('properties').get('practice_1_extent') if _period.get('properties').get('practice_1_extent') else 0
                planned_practice_2_extent = _period.get('properties').get('practice_2_extent') if _period.get('properties').get('practice_2_extent') else 0
                planned_practice_3_extent = _period.get('properties').get('practice_3_extent') if _period.get('properties').get('practice_3_extent') else 0
                planned_practice_4_extent = _period.get('properties').get('practice_4_extent') if _period.get('properties').get('practice_4_extent') else 0

                planned_impervious_area = _period.get('properties').get('impervious_area') if _period.get('properties').get('impervious_area') else 0
                planned_total_drainage_area = _period.get('properties').get('total_drainage_area') if _period.get('properties').get('total_drainage_area') else 0

            elif _period.get('properties').get('measurement_period') == 'Installation':
                installed_total_nitrogen += _period.get('properties').get('installation').get('nitrogen', 0).get('value', 0)
                installed_total_phosphorus += _period.get('properties').get('installation').get('phosphorus', 0).get('value', 0)
                installed_total_sediment += _period.get('properties').get('installation').get('sediment', 0).get('value', 0)
                installed_gallons_per_year_of_stormwater_detained_or_infiltrated += _period.get('properties').get('metrics').get('gallons_per_year_of_stormwater_detained_or_infiltrated', 0)
                installed_acres_of_protected_bmps_to_reduce_stormwater_runoff += _period.get('properties').get('metrics').get('acres_of_protected_bmps_to_reduce_stormwater_runoff', 0)
                installed_acres_of_installed_bmps_to_reduce_stormwater_runoff += _period.get('properties').get('metrics').get('acres_of_installed_bmps_to_reduce_stormwater_runoff', 0)

                installed_practice_1_extent = _period.get('properties').get('practice_1_extent') if _period.get('properties').get('practice_1_extent') else 0
                installed_practice_2_extent = _period.get('properties').get('practice_2_extent') if _period.get('properties').get('practice_2_extent') else 0
                installed_practice_3_extent = _period.get('properties').get('practice_3_extent') if _period.get('properties').get('practice_3_extent') else 0
                installed_practice_4_extent = _period.get('properties').get('practice_4_extent') if _period.get('properties').get('practice_4_extent') else 0
                installed_impervious_area = _period.get('properties').get('impervious_area') if _period.get('properties').get('impervious_area') else 0
                installed_total_drainage_area = _period.get('properties').get('total_drainage_area') if _period.get('properties').get('total_drainage_area') else 0

        _totals = {
            'nitrogen': installed_total_nitrogen,
            'phosphorus': installed_total_phosphorus,
            'sediment': installed_total_sediment,
            'gallons_per_year_of_stormwater_detained_or_infiltrated': installed_gallons_per_year_of_stormwater_detained_or_infiltrated,
            'acres_of_protected_bmps_to_reduce_stormwater_runoff': installed_acres_of_protected_bmps_to_reduce_stormwater_runoff,
            'acres_of_installed_bmps_to_reduce_stormwater_runoff': installed_acres_of_installed_bmps_to_reduce_stormwater_runoff,

            'practice_1_extent': installed_practice_1_extent,
            'practice_2_extent': installed_practice_2_extent,
            'practice_3_extent': installed_practice_3_extent,
            'practice_4_extent': installed_practice_4_extent,

            'impervious_area': installed_impervious_area,
            'total_drainage_area': installed_total_drainage_area,
        }

        if percentage:
            _totals = {
                'nitrogen': (installed_total_nitrogen/planned_total_nitrogen)*100 if planned_total_nitrogen > 0 else 0,
                'phosphorus': (installed_total_phosphorus/planned_total_phosphorus)*100 if planned_total_phosphorus > 0 else 0,
                'sediment': (installed_total_sediment/planned_total_sediment)*100 if planned_total_sediment > 0 else 0,

                'gallons_per_year_of_stormwater_detained_or_infiltrated': (installed_acres_of_protected_bmps_to_reduce_stormwater_runoff/planned_acres_of_protected_bmps_to_reduce_stormwater_runoff)*100 if planned_acres_of_protected_bmps_to_reduce_stormwater_runoff > 0 else 0,
                'acres_of_protected_bmps_to_reduce_stormwater_runoff': (installed_acres_of_protected_bmps_to_reduce_stormwater_runoff/planned_acres_of_protected_bmps_to_reduce_stormwater_runoff)*100 if planned_acres_of_protected_bmps_to_reduce_stormwater_runoff > 0 else 0,
                'acres_of_installed_bmps_to_reduce_stormwater_runoff': (installed_acres_of_installed_bmps_to_reduce_stormwater_runoff/planned_acres_of_installed_bmps_to_reduce_stormwater_runoff)*100 if planned_acres_of_installed_bmps_to_reduce_stormwater_runoff > 0 else 0,

                'practice_1_extent': (installed_practice_1_extent/planned_practice_1_extent)*100 if planned_practice_1_extent > 0 else 0,
                'practice_2_extent': (installed_practice_2_extent/planned_practice_2_extent)*100 if planned_practice_2_extent > 0 else 0,
                'practice_3_extent': (installed_practice_3_extent/planned_practice_3_extent)*100 if planned_practice_3_extent > 0 else 0,
                'practice_4_extent': (installed_practice_4_extent/planned_practice_4_extent)*100 if planned_practice_4_extent > 0 else 0,

                'impervious_area': (installed_impervious_area/planned_impervious_area)*100 if planned_impervious_area > 0 else 0,
                'total_drainage_area': (installed_total_drainage_area/planned_total_drainage_area)*100 if planned_total_drainage_area > 0 else 0,
            }

        return _totals

    def adjustorCurveNitrogen(self, value):

        depthTreated = self.runoffDepthTreated(value)
        runoffVolumeCaptured = self.runoffVolumeCaptured(value)

        classification = value.get('site_reduction_classification', None)
        reduction = 0

        if classification == "Runoff Reduction":
            first = 0.0308*Math.pow(depthTreated, 5)
            second = 0.2562*Math.pow(depthTreated, 4)
            third = 0.8634*Math.pow(depthTreated, 3)
            fourth = 1.5285*Math.pow(depthTreated, 2)
            fifth = 1.501*depthTreated

            reduction = (first-second+third-fourth+fifth-0.013)

        elif classification == "Stormwater Treatment":
            first = 0.0152*Math.pow(depthTreated, 5)
            second = 0.131*Math.pow(depthTreated, 4)
            third = 0.4581*Math.pow(depthTreated, 3)
            fourth = 0.8418*Math.pow(depthTreated, 2)
            fifth = 0.8536*depthTreated

            reduction = (first-second+third-fourth+fifth-0.0046)

        return reduction

    def adjustorCurvePhosphorus(self, value):

        depthTreated = self.runoffDepthTreated(value)
        runoffVolumeCaptured = self.runoffVolumeCaptured(value)

        classification = value.get('site_reduction_classification', None)
        reduction = 0

        if classification == "Runoff Reduction":
            first = 0.0304*Math.pow(depthTreated, 5)
            second = 0.2619*Math.pow(depthTreated, 4)
            third = 0.9161*Math.pow(depthTreated, 3)
            fourth = 1.6837*Math.pow(depthTreated, 2)
            fifth = 1.7072*depthTreated

            reduction = (first-second+third-fourth+fifth-0.0091)

        elif classification == "Stormwater Treatment":
            first = 0.0239*Math.pow(depthTreated, 5)
            second = 0.2058*Math.pow(depthTreated, 4)
            third = 0.7198*Math.pow(depthTreated, 3)
            fourth = 1.3229*Math.pow(depthTreated, 2)
            fifth = 1.3414*depthTreated

            reduction = (first-second+third-fourth+fifth-0.0072)

        return reduction

    def adjustorCurveSediment(self, value):

        depthTreated = self.runoffDepthTreated(value)
        runoffVolumeCaptured = self.runoffVolumeCaptured(value)

        classification = value.get('site_reduction_classification', None)
        reduction = 0

        if classification == "Runoff Reduction":
            first = 0.0326*Math.pow(depthTreated, 5)
            second = 0.2806*Math.pow(depthTreated, 4)
            third = 0.9816*Math.pow(depthTreated, 3)
            fourth = 1.8039*Math.pow(depthTreated, 2)
            fifth = 1.8292*depthTreated

            reduction = (first-second+third-fourth+fifth-0.0098)

        elif classification == "Stormwater Treatment":
            first = 0.0304*Math.pow(depthTreated, 5)
            second = 0.2619*Math.pow(depthTreated, 4)
            third = 0.9161*Math.pow(depthTreated, 3)
            fourth = 1.6837*Math.pow(depthTreated, 2)
            fifth = 1.7072*depthTreated

            reduction = (first-second+third-fourth+fifth-0.0091)

        return reduction

    def nitrogen(self, value, loaddata, preinstallation=False):

        multiplier = 1

        if preinstallation == False:
            multiplier = self.adjustorCurveNitrogen(value)

        impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0
        impervious_tn_ual = loaddata['impervious']['tn_ual'] if loaddata and 'impervious' in loaddata and 'tn_ual' in loaddata['impervious'] else 0
        total_drainage_area = value.get('total_drainage_area') if value.get('total_drainage_area') else 0

        return {
            "value": (((impervious_area*impervious_tn_ual) + ((total_drainage_area-impervious_area)*impervious_tn_ual))*multiplier)/43560,
            "adjustor": multiplier
        }

    def phosphorus(self, value, loaddata, preinstallation=False):

        multiplier = 1

        if preinstallation == False:
            multiplier = self.adjustorCurvePhosphorus(value)

        impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0
        impervious_tp_ual = loaddata['impervious']['tp_ual'] if loaddata and 'impervious' in loaddata and 'tp_ual' in loaddata['impervious'] else 0
        total_drainage_area = value.get('total_drainage_area') if value.get('total_drainage_area') else 0

        return {
            "value": (((impervious_area*impervious_tp_ual) + ((total_drainage_area-impervious_area)*impervious_tp_ual))*multiplier)/43560,
            "adjustor": multiplier
        }

    def sediment(self, value, loaddata, preinstallation=False):

        multiplier = 1

        if preinstallation == False:
            multiplier = self.adjustorCurveSediment(value)

        impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0
        impervious_tss_ual = loaddata['impervious']['tss_ual'] if loaddata and 'impervious' in loaddata and 'tss_ual' in loaddata['impervious'] else 0
        total_drainage_area = value.get('total_drainage_area') if value.get('total_drainage_area') else 0

        return {
            "value": (((impervious_area*impervious_tss_ual) + ((total_drainage_area-impervious_area)*impervious_tss_ual))*multiplier)/43560,
            "adjustor": multiplier
        }

    def runoffDepthTreated(self, value):

        depthTreated = 1.0

        runoff_volume_captured = value.get('runoff_volume_captured') if value.get('runoff_volume_captured') else 0
        impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0

        if runoff_volume_captured and impervious_area:
          depthTreated = (runoff_volume_captured*12)/(impervious_area/43560)

        return depthTreated

    def rainfallDepthTreated(self, value):
        depthTreated = self.runoffDepthTreated(value)
        impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0
        return (depthTreated/(impervious_area/43560))*12

    def runoffVolumeCaptured(self, value):
        depthTreated = self.runoffDepthTreated(value)
        impervious_area = value.get('impervious_area') if value.get('impervious_area') else 0
        return (depthTreated*impervious_area)/(12*43560)

    def acres_of_protected_bmps_to_reduce_stormwater_runoff(self, value):
        total_drainage_area = value.get('total_drainage_area') if value.get('total_drainage_area') else 0
        return (total_drainage_area/43560)

    def acres_of_installed_bmps_to_reduce_stormwater_runoff(self, value):

        practice_1_extent = value.get('practice_1_extent') if value.get('practice_1_extent') else 0
        practice_2_extent = value.get('practice_2_extent') if value.get('practice_2_extent') else 0
        practice_3_extent = value.get('practice_3_extent') if value.get('practice_3_extent') else 0
        practice_4_extent = value.get('practice_4_extent') if value.get('practice_4_extent') else 0

        return practice_1_extent+practice_2_extent+practice_3_extent+practice_4_extent;

    def gallons_per_year_of_stormwater_detained_or_infiltrated(self, value):

        gallons_ = 0

        runoff_volume_captured = value.get('runoff_volume_captured') if value.get('runoff_volume_captured') else 0

        if runoff_volume_captured:
          gallons_ = (runoff_volume_captured*325851.4)

        return gallons_
