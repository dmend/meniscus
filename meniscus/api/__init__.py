import falcon
from meniscus.openstack.common import jsonutils


class ApiResource(object):
    """
    Base class for API resources
    """
    pass


def abort(status=falcon.HTTP_500, message=None):
    """
    Helper function for aborting an API request process. Useful for error
    reporting and exception handling.
    """
    raise falcon.HTTPError(status, message)


def load_body(req, required=[]):
    """
    Helper function for loading an HTTP request body from JSON into a
    Python dictionary
    """
    try:
        raw_json = req.stream.read()

    except Exception:
        abort(falcon.HTTP_500, 'Read Error')

    try:
        parsed_body = jsonutils.loads(raw_json)
        return parsed_body
    except ValueError as ve:
        abort(falcon.HTTP_400, 'Malformed JSON')


def format_response_body(body):
    """
    Helper function for formatting the response body as JSON into a
    Python dictionary
    """
    return jsonutils.dumps(body)
