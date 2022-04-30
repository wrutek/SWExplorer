import requests


def get_request(url, params=None):
    """
    Send a GET request to the specified URL.

    TOOO: there is a lot to do here.
    - response validation
    - proper handling, redirects to the right error page (maybe even a regular page with message modal)
    - custom (per request url) validation
    - custom (per request url) error handling
    """
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        return resp.json()
    raise Http400("SWAPI error")


class Http400(Exception):
    """
    Custom exception for HTTP 400 errors.
    """
    pass
