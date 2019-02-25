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

# Import Flask dependencies

from flask import jsonify


class Responses(object):
    """Ready to Use JSON Status Responses.

    :param object object: For a full explanation please see
    https://docs.python.org/release/2.2.3/whatsnew/sect-rellinks.html

    For more information regarding HTTP Hypertext Transfer Protocol
    Status Code Definitions see the official RFC 2616 documentation
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    """

    def __init__(self, response_format='json'):
        """Initialize top level variables."""
        self.response_format = response_format

    def __repr__(self):
        """Display of VIStatus when inspected."""
        return '<VIStatus responses>'

    def status_100(self, message=''):
        """HTTP Status Code 100."""
        return jsonify(**{
            'meta': {
                'code': 100,
                'status': 'Continue'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_101(self, message=''):
        """HTTP Status Code 101."""
        return jsonify(**{
            'meta': {
                'code': 101,
                'status': 'Switching Protocol'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_200(self, message=''):
        """HTTP Status Code 200."""
        return jsonify(**{
            'meta': {
                'code': 200,
                'status': 'OK'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_201(self, message=''):
        """HTTP Status Code 201."""
        return jsonify(**{
            'meta': {
                'code': 201,
                'status': 'Created'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_202(self, message=''):
        """HTTP Status Code 202."""
        return jsonify(**{
            'meta': {
                'code': 202,
                'status': 'Accepted'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_203(self, message=''):
        """HTTP Status Code 203."""
        return jsonify(**{
            'meta': {
                'code': 203,
                'status': 'Non-Authoritative Information'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_204(self, message=''):
        """HTTP Status Code 204."""
        return jsonify(**{
            'meta': {
                'code': 204,
                'status': 'No Content'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_205(self, message=''):
        """HTTP Status Code 205."""
        return jsonify(**{
            'meta': {
                'code': 205,
                'status': 'Reset Content'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_206(self, message=''):
        """HTTP Status Code 206."""
        return jsonify(**{
            'meta': {
                'code': 206,
                'status': 'Partial Content'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_300(self, message=''):
        """HTTP Status Code 300."""
        return jsonify(**{
            'meta': {
                'code': 300,
                'status': 'Multiple Choice'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_301(self, message=''):
        """HTTP Status Code 301."""
        return jsonify(**{
            'meta': {
                'code': 301,
                'status': 'Moved Permanently'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_302(self, message=''):
        """HTTP Status Code 302."""
        return jsonify(**{
            'meta': {
                'code': 302,
                'status': 'Found'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_303(self, message=''):
        """HTTP Status Code 303."""
        return jsonify(**{
            'meta': {
                'code': 303,
                'status': 'See Other'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_304(self, message=''):
        """HTTP Status Code 304."""
        return jsonify(**{
            'meta': {
                'code': 304,
                'status': 'Not Modified'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_305(self, message=''):
        """HTTP Status Code 305."""
        return jsonify(**{
            'meta': {
                'code': 305,
                'status': 'Use Proxy'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_307(self, message=''):
        """HTTP Status Code 307."""
        return jsonify(**{
            'meta': {
                'code': 307,
                'status': 'Temporary Redirect'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_308(self, message=''):
        """HTTP Status Code 308."""
        return jsonify(**{
            'meta': {
                'code': 308,
                'status': 'Permanent Redirect'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_400(self, message=''):
        """HTTP Status Code 400."""
        return jsonify(**{
            'meta': {
                'code': 400,
                'status': 'Bad Request'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_401(self, message=''):
        """HTTP Status Code 401."""
        return jsonify(**{
            'meta': {
                'code': 401,
                'status': 'Unauthorized'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_402(self, message=''):
        """HTTP Status Code 402."""
        return jsonify(**{
            'meta': {
                'code': 402,
                'status': 'Payment Required'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_403(self, message=''):
        """HTTP Status Code 403."""
        return jsonify(**{
            'meta': {
                'code': 403,
                'status': 'Forbidden'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_404(self, message=''):
        """HTTP Status Code 404."""
        return jsonify(**{
            'meta': {
                'code': 404,
                'status': 'Page Not Found'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_405(self, message=''):
        """HTTP Status Code 405."""
        return jsonify(**{
            'meta': {
                'code': 405,
                'status': 'Method Not Allowed'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_406(self, message=''):
        """HTTP Status Code 406."""
        return jsonify(**{
            'meta': {
                'code': 406,
                'status': 'Not Acceptable'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_407(self, message=''):
        """HTTP Status Code 407."""
        return jsonify(**{
            'meta': {
                'code': 407,
                'status': 'Proxy Authentication Required'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_408(self, message=''):
        """HTTP Status Code 408."""
        return jsonify(**{
            'meta': {
                'code': 408,
                'status': 'Request Timeout'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_409(self, message=''):
        """HTTP Status Code 409."""
        return jsonify(**{
            'meta': {
                'code': 409,
                'status': 'Conflict'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_410(self, message=''):
        """HTTP Status Code 410."""
        return jsonify(**{
            'meta': {
                'code': 410,
                'status': 'Gone'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_411(self, message=''):
        """HTTP Status Code 411."""
        return jsonify(**{
            'meta': {
                'code': 411,
                'status': 'Length Required'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_412(self, message=''):
        """HTTP Status Code 412."""
        return jsonify(**{
            'meta': {
                'code': 412,
                'status': 'Precondition Failed'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_413(self, message=''):
        """HTTP Status Code 413."""
        return jsonify(**{
            'meta': {
                'code': 413,
                'status': 'Payload Too Large'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_414(self, message=''):
        """HTTP Status Code 414."""
        return jsonify(**{
            'meta': {
                'code': 414,
                'status': 'URI Too Long'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_415(self, message=''):
        """HTTP Status Code 415."""
        return jsonify(**{
            'meta': {
                'code': 415,
                'status': 'Unsupported Media Type'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_416(self, message=''):
        """HTTP Status Code 416."""
        return jsonify(**{
            'meta': {
                'code': 416,
                'status': 'Request Range Not Satisifible'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_417(self, message=''):
        """HTTP Status Code 417."""
        return jsonify(**{
            'meta': {
                'code': 417,
                'status': 'Expectation Failed'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_418(self, message=''):
        """HTTP Status Code 418."""
        return jsonify(**{
            'meta': {
                'code': 418,
                'status': 'I\'m a teapot'
            },
            'response': {
                'message': 'Any attempt to brew coffee with a teapot should'
                           'result in the error code "418 I\'m a teapot".'
                           'resulting entity body MAY be short and stout.'
            }
        })

    def status_421(self, message=''):
        """HTTP Status Code 421."""
        return jsonify(**{
            'meta': {
                'code': 421,
                'status': 'Misdirected Request'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_426(self, message=''):
        """HTTP Status Code 426."""
        return jsonify(**{
            'meta': {
                'code': 426,
                'status': 'Upgrade Required'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_428(self, message=''):
        """HTTP Status Code 428."""
        return jsonify(**{
            'meta': {
                'code': 428,
                'status': 'Precondition Required'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_429(self, message=''):
        """HTTP Status Code 429."""
        return jsonify(**{
            'meta': {
                'code': 429,
                'status': 'Too Many Requests'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_431(self, message=''):
        """HTTP Status Code 431."""
        return jsonify(**{
            'meta': {
                'code': 431,
                'status': 'Request Header Fields Too Large'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_500(self, message=''):
        """HTTP Status Code 500."""
        return jsonify(**{
            'meta': {
                'code': 500,
                'status': 'Internal Server Error'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_501(self, message=''):
        """HTTP Status Code 501."""
        return jsonify(**{
            'meta': {
                'code': 501,
                'status': 'Not Implemented'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_502(self, message=''):
        """HTTP Status Code 502."""
        return jsonify(**{
            'meta': {
                'code': 502,
                'status': 'Bad Gateway'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_503(self, message=''):
        """HTTP Status Code 503."""
        return jsonify(**{
            'meta': {
                'code': 503,
                'status': 'Service Unavailable'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_504(self, message=''):
        """HTTP Status Code 504."""
        return jsonify(**{
            'meta': {
                'code': 504,
                'status': 'Gateway Timeout'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_505(self, message=''):
        """HTTP Status Code 505."""
        return jsonify(**{
            'meta': {
                'code': 505,
                'status': 'HTTP Version Not Supported'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_506(self, message=''):
        """HTTP Status Code 506."""
        return jsonify(**{
            'meta': {
                'code': 506,
                'status': 'Variant Also Negotiates'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_507(self, message=''):
        """HTTP Status Code 507."""
        return jsonify(**{
            'meta': {
                'code': 507,
                'status': 'Variant Also Negotiates'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })

    def status_511(self, message=''):
        """HTTP Status Code 511."""
        return jsonify(**{
            'meta': {
                'code': 511,
                'status': 'Network Authentication Required'
            },
            'response': {
                'message': str(message) if message else ''
            }
        })
