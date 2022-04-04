#!/usr/bin/env python


import os

from flask import Blueprint


static_folder = os.path.join(os.pardir, 'static')

module = Blueprint(**{
    'name': __name__,
    'import_name': __name__,
    'static_folder': None,
    'static_url_path': None,
    'template_folder': None,
    'url_prefix': None,
    'subdomain': None,
    'url_defaults': None
})

if module:
    """Verify module Blueprint is instantiated."""
    from . import views
