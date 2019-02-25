#!/usr/bin/env python

"""Modules package.

Created by Viable Industries, L.L.C. on 01/26/2015.
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

# Import package dependencies

from app.schema.practice_type import PracticeType
from app.schema.tag import Tag


FILTER_MAP = {
    'organization': lambda a, b: a.append(
        PracticeType.organization_id.in_(b)
    ),
    'program': lambda a, b: a.append(
        PracticeType.program_id.in_(b)
    ),
    'tag': lambda a, b: a.append(
        PracticeType.tags.any(
            Tag.id.in_(b))
    )
}