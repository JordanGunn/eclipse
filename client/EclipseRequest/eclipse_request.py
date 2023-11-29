# system imports
import json
from typing import Union
from requests import get, post

# user imports
from eclipse_table import EclipseTable


class EclipseHttpMethods:

    """Supported HTTP Methods for Eclipse"""

    GET = "GET"
    POST = "POST"
    LIST = [GET, POST]


class EclipseRequest:

    ENDPOINT = "/eclipse/api/"

    def __init__(self, http_method: str):

        self.http_method = http_method.upper()
        self.data = None

    def send(self, endpoint: str, data: Union[str, dict]) -> str:
        """
        Send handler for EclipseRequest.

        :param endpoint: Eclipse endpoint - corresponds to db table.
        :param data: url query parameters (for GET), or json data (for POST).

        :return: HTTP Response as JSON str, or empty string on failure.
        """

        res = ""
        if self.http_method == EclipseHttpMethods.GET:
            res = self._get(endpoint, data)
        if self.http_method == EclipseHttpMethods.POST:
            res = self._post(endpoint, data)

        return res

    def _get(self, endpoint: str, params: dict = None) -> str:

        """
        Generic GET request handler.
        """

        # make sure separators are correct
        ep = endpoint.replace("/", "")
        url = self.ENDPOINT + "/" + ep

        res = get(url, params=params)
        return res.json()

    def _post(self, endpoint: str, data: Union[str, dict]) -> str:

        """
        Generic POST request handler.
        """

        # make sure separators are correct
        tbl = endpoint.replace("/", "")
        url = self.ENDPOINT + "/" + tbl + "/"
        if not url.endswith("/"):
            url += "/"

        if isinstance(data, str):
            # convert json string to dict
            data = json.dumps(data, indent=4)

        res = post(url, json=data)
        return res.json()








