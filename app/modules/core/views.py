#!/usr/bin/env python

from flask import jsonify
from flask import request

from . import module
from . import utilities


@module.route('/v1/analyze', methods=['OPTIONS'])
def analyze_options():

    """Define default user preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    })


@module.route('/v1/analyze', methods=['POST'])
def analyze_post():

    datum = utilities.handle_request(
        request.get_json())

    return jsonify(**datum), 200
