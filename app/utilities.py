#!/usr/bin/env python

import functools
import math
import operator
import re
from datetime import datetime

from sqlalchemy import inspect


def unix_time(obj):
    """
    Represent a datetime object in milliseconds
    since the Unix epoch (1970-01-01 00:00:00).

    :param obj: A datetime object. Note that no
    support is provided for time zones. Stored
    values throughout the system follow the UTC
    standard.
    """

    epoch = datetime.utcfromtimestamp(0)

    return int((obj - epoch).total_seconds()) * 1000


def normalize_string(text=None):

    """
    Remove all non-alphanumeric chars from the input string.

    Apply str.lower() and str.strip() before executing re.sub().
    """

    if text:

        _text = '_'.join(text.lower().strip().split())

        return re.sub(r'[\W]+', '', _text, re.UNICODE)

    return ''


def precision_round(value, decimals, base=10):

    exp = math.pow(base, decimals)

    return round(value * exp) / exp


def truncate(text, length):

    #: Conditional will be falsey if
    #: text is None or empty string.

    if text and isinstance(text, basestring):

        return text[:length]

    return None


def parse_snake(text, operation=None):

    #: Conditional will be falsey if
    #: text is None or empty string.

    if text and isinstance(text, basestring):

        _tpl = text.replace('_', ' ')

        if operation == 'capitalize':

            _tpl.capitalize()

        elif operation == 'lower':

            _tpl.lower()

        elif operation == 'title':

            _tpl.title()

        elif operation == 'upper':

            _tpl.upper()

        return _tpl

    return None


def scrub_request(model, data):

    insp = inspect(model)

    whitelist = [
        attr for attr in insp.all_orm_descriptors.keys()
        if not(attr.startswith('_'))
    ]

    inputs = data.keys()

    for attribute in inputs:

        if attribute not in whitelist:

            data.pop(attribute, None)

    return data


def rgetattr(obj, attr, *args):
    """See https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects"""
    def _getattr(obj, attr):

        return getattr(obj, attr, *args)

    return reduce(_getattr, [obj] + attr.split('.'))


def product(seq):
    """
    Multiply a list of values.

    :param seq: A list of numeric values.
    :return: Multiplication product.
    """

    return functools.reduce(operator.mul, seq)
