"""Testing environment configuration settings.

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


from .config import Config


class TestingConfig(Config):
    """Testing environment configuration settings.

    @param (object) Config
        The primary Config class which we are subclassing
    """

    """FlaskSQLAlchemy Configuration.

    See the official Flask SQLAlchemy documentation for more information
    http://flask-sqlalchemy.pocoo.org/2.1/config/
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://127.0.0.1:5432/dnr_model'
