# #!/usr/bin/env python

# """Define the Unit schema.

# Created by Viable Industries, L.L.C. on 02/10/2018.
# Copyright (c) 2018 Viable Industries, L.L.C. All rights reserved.

# For license and copyright information please see the LICENSE document (the
# "License") included with this software package. This file may not be used
# in any manner except in compliance with the License unless required by
# applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.

# See the License for the specific language governing permissions and
# limitations under the License.
# """

# # Import package dependencies

# from app import db
# from app import logger

# from app.permissions import *
# from app.utilities import parse_snake


# class UnitGroup(db.Model):

#     __public__ = []

#     """
#     Name of the database table that holds `UnitGroup` data

#     @see http://docs.sqlalchemy.org/en/rel_0_9/orm/maps/declarative.html#table-configuration
#     """
#     __tablename__ = 'unit_group'
#     __table_args__ = {
#         'extend_existing': True
#     }

#     """
#     Fields within the data model
#     """
#     name = db.Column(db.Text, primary_key=True)


# class Unit(db.Model):
#     """Unit schema definition.

#     The `Unit` database table definition.

#     :param object db.Model: SQLAlchemy declarative base

#     See the official Flask SQLAlchemy documentation for more information
#     https://pythonhosted.org/Flask-SQLAlchemy/models.html
#     """

#     __tablename__ = 'unit'
#     __table_args__ = {
#         'extend_existing': True
#     }

#     id = db.Column(db.Integer, primary_key=True)
#     singular = db.Column(db.Text, unique=True)
#     plural = db.Column(db.Text)
#     description = db.Column(db.Text)
#     usage = db.Column(db.Text)
#     symbol = db.Column(db.Text)

#     # `UnitGroup` relation to associate with this feature.

#     group = db.Column(db.Text,
#         db.ForeignKey('unit_group.name',
#             onupdate='CASCADE'))

#     #: Specify fields that should be available to keyword searches

#     search_fields = [
#         'plural',
#         'singular',
#         'description',
#         'usage'
#     ]

#     #: Specify default filter conditions

#     @classmethod
#     def filter_preset(cls):

#         return []


#     def build_label(self):

#         return u'%s \u00B7 %s' % (self.symbol, self.plural)


#     def search_result(self, q=None):

#         return {
#             'id': self.id,
#             'category': parse_snake(self.__tablename__),
#             'name': self.build_label(),
#             'subcategory': None
#         }
