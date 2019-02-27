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

from app.modules import bank_stabilization
from app.modules import enhanced_stream_restoration
from app.modules import instream_habitat
from app.modules import stormwater


FUNC_IDX = {
    'bank_stabilization': bank_stabilization.utilities.reduction,
    'enhanced_stream_restoration': enhanced_stream_restoration.utilities.reduction,
    'instream_habitat': instream_habitat.utilities,
    'stormwater': stormwater.utilities.reduction
}
