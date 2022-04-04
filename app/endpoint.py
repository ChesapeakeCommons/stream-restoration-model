#!/usr/bin/env python

from app import logger


class Endpoint(object):
    """Define the default Endpoint scaffold.

    The Endpoint scaffold creates a set of defaults to quickly get us started
    creating new module endpoints (e.g.,
    `app/modules/<:myModule>/<:myendpoint.py>). This class defines an object
    capable of being loaded by the Flask-Restless package.

    See the official Flask Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/
    """

    """Define all base preprocessors.

    https://flask-restless.readthedocs.org/en/latest/customizing.html\
    #request-preprocessors-and-postprocessors
    """

    def base_preprocessor_get_single(instance_id=None, **kw):
        """Create a generic GET_SINGLE preprocessor.

        Accepts a single argument, `instance_id`, the primary key of the
        instance of the model to get.
        """
        logger.info('`base_preprocessor_get_single` responded to request')

    def base_preprocessor_get_many(search_params=None, **kw):
        """Create a generic GET_MANY preprocessor.

        Accepts a single argument, `search_params`, which is a dictionary
        containing the search parameters for the request.
        """
        logger.info('`base_preprocessor_get_many` responded to request')

    def base_preprocessor_update_single(instance_id=None, **kw):
        """Create a generic PATCH_SINGLE and PUT_SINGLE preprocessor.

        Accepts two arguments, `instance_id`, the primary key of the
        instance of the model to patch, and `data`, the dictionary of fields
        to change on the instance.
        """
        logger.info('`base_preprocessor_update_single` used for endpoint')

    def base_preprocessor_update_many(search_params=None, **kw):
        """Create a generic PATCH_MANY and PATCH_SINGLE preprocessor.

        Accepts two arguments: `search_params`, which is a dictionary
        containing the search parameters for the request, and `data`, which
        is a dictionary representing the fields to change on the matching
        instances and the values to which they will be set.
        """
        logger.info('`base_preprocessor_update_many` used for endpoint')

    def base_preprocessor_post(data=None, **kw):
        """Create a generic POST preprocessor.

        Accepts a single argument, `data`, which is the dictionary of
        fields to set on the new instance of the model.
        """
        logger.info('`base_preprocessor_post` used for endpoint')

    def base_preprocessor_delete_single(instance_id=None, **kw):
        """Create a generic DELETE_SINGLE preprocessor.

        Accepts a single argument, `instance_id`, which is the primary key
        of the instance which will be deleted.
        """
        logger.info('`base_preprocessor_delete_single` used for endpoint')

    def base_preprocessor_delete_many(search_params=None, **kw):
        """Create a generic DELETE_MANY preprocessor.

        Accepts a single argument, `search_params`, which is a dictionary
        containing the search parameters for the request.
        """
        logger.info('`base_preprocessor_delete_many` used for endpoint')

    """Define all base postprocessors.

    https://flask-restless.readthedocs.org/en/latest/customizing.html\
    #request-preprocessors-and-postprocessors
    """

    def base_postprocessor_get_single(result=None, **kw):
        """Create a generic GET_SINGLE postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the requested instance of the model.
        """
        logger.info('`base_postprocessor_get_single` responded to request')

    def base_postprocessor_get_many(result=None, search_params=None, **kw):
        """Create a generic GET_MANY postprocessor.

        Accepts two arguments, `result`, which is the dictionary
        representation of the JSON response which will be returned to the
        client, and `search_params`, which is a dictionary containing the
        search parameters for the request (that produced the specified
        `result`).
        """
        logger.info('`base_postprocessor_get_many` responded to request')

    def base_postprocessor_update_single(result=None, **kw):
        """Create a generic PATCH_SINGLE and PUT_SINGLE postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the requested instance of the model.
        """
        logger.info('`base_postprocessor_update_single` used for endpoint')

    def base_postprocessor_update_many(query=None, data=None,
                                       search_params=None, **kw):
        """Create a generic PATCH_MANY and PATCH_SINGLE postprocessor.

        Accepts three arguments: `query`, which is the SQLAlchemy query
        which was inferred from the search parameters in the query string,
        `data`, which is the dictionary representation of the JSON response
        which will be returned to the client, and `search_params`, which is a
        dictionary containing the search parameters for the request.
        """
        logger.info('`base_postprocessor_update_many` used for endpoint')

    def base_postprocessor_post(result=None, **kw):
        """Create a generic POST postprocessor.

        Accepts a single argument, `result`, which is the dictionary
        representation of the created instance of the model.
        """
        logger.info('`base_postprocessor_post` used for endpoint')

    def base_postprocessor_delete_single(was_deleted=None, **kw):
        """Create a generic DELETE_SINGLE postprocessor.

        Accepts a single argument, `was_deleted`, which represents whether
        the instance has been deleted.
        """
        logger.info('`base_postprocessor_delete_single` used for endpoint')

    def base_postprocessor_delete_many(result=None, search_params=None, **kw):
        """Create a generic DELETE_MANY postprocessor.

        Accepts two arguments: `result`, which is the dictionary
        representation of which is the dictionary representation of the JSON
        response which will be returned to the client, and `search_params`,
        which is a dictionary containing the search parameters for the
        request.
        """
        logger.info('`base_postprocessor_delete_many` used for endpoint')

    """Flask-Restless Endpoint Arguments.

    These arguments define how the endpoint will be setup. These are the
    defaults that we will use. These arguments can be overridden once a new
    Endpoint class has been instantiated.

    See the official Flask-Restless documentation for more information
    https://flask-restless.readthedocs.org/en/latest/api.html#\
    flask.ext.restless.APIManager.create_api_blueprint
    """
    __arguments__ = {
        'url_prefix': '/v1/data',
        'exclude_columns': [],
        'max_results_per_page': 500,
        'methods': [
            'GET',
            'POST',
            'PATCH',
            'PUT',
            'DELETE'
        ],
        'preprocessors': {
            'GET_SINGLE': [base_preprocessor_get_single],
            'GET_MANY': [base_preprocessor_get_many],
            'PUT_SINGLE': [base_preprocessor_update_single],
            'PUT_MANY': [base_preprocessor_update_many],
            'PATCH_SINGLE': [base_preprocessor_update_single],
            'PATCH_MANY': [base_preprocessor_update_many],
            'POST': [base_preprocessor_post],
            'DELETE_SINGLE': [base_preprocessor_delete_single],
            'DELETE_MANY': [base_preprocessor_delete_many]
        },
        'postprocessors': {
            'GET_SINGLE': [base_postprocessor_get_single],
            'GET_MANY': [base_postprocessor_get_many],
            'PUT_SINGLE': [base_postprocessor_update_single],
            'PUT_MANY': [base_postprocessor_update_many],
            'PATCH_SINGLE': [base_postprocessor_update_single],
            'PATCH_MANY': [base_postprocessor_update_many],
            'POST': [base_postprocessor_post],
            'DELETE_SINGLE': [base_postprocessor_delete_single],
            'DELETE_MANY': [base_postprocessor_delete_many]
        },
        'allow_functions': True,
        'allow_patch_many': False
    }
