#!/usr/bin/env python

"""Define the Practice Type schema.

Created by Viable Industries, L.L.C. on 02/10/2018.
Copyright (c) 2018 Viable Industries, L.L.C. All rights reserved.

For license and copyright information please see the LICENSE document (the
"License") included with this software package. This file may not be used
in any manner except in compliance with the License unless required by
applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""

# Import package dependencies

from app import db
from app import logger

from app.utilities import parse_snake


class Practice(db.Model):
    """Practice schema definition.

    The `Practice` database table definition.

    :param object db.Model: SQLAlchemy declarative base

    See the official Flask SQLAlchemy documentation for more information
    https://pythonhosted.org/Flask-SQLAlchemy/models.html
    """

    __tablename__ = 'practice'
    __table_args__ = {
        'extend_existing': True
    }

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text)
    description = db.Column(db.Text)
    key = db.Column(db.Text, unique=True)

    # Specify fields that should be available to keyword searches

    search_fields = [
        'name'
    ]

    def search_result(self, q=None):

        return {
            'id': self.id,
            'category': parse_snake(self.__tablename__),
            'name': self.name,
            'subcategory': None
        }
