#!/usr/bin/env python


from flask import Blueprint


module = Blueprint(**{
    'name': __name__,
    'import_name': __name__,
    'static_folder': None,
    'static_url_path': None,
    'template_folder': 'templates',
    'url_prefix': None,
    'subdomain': None,
    'url_defaults': None
})

if module:
    """Verify module Blueprint is instantiated."""
    from . import utilities
