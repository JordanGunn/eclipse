# system imports
import json
import requests
from typing import Union
from urllib.parse import urljoin

# user imports
from client.entity.entity import Entity
from client.entity.entity_attrs import ENTITY_ATTR_MAP


class EclipseHttpMethod:

    """Valid http methods enabled for eclipse"""

    GET = "GET"
    POST = "POST"
    LIST = [GET, POST]


class EclipseRequest:

    """Abstract parent to various Eclipse Request objects"""

    _ENDPOINT = "/api/"

    def __init__(self, http_method: str, entity: Entity, url_params: Union[dict, None]):

        if http_method.upper() not in EclipseHttpMethod.LIST:
            raise ValueError(f"Unsupported HTTP method: {http_method}")

        self._entity = entity
        self.http_method = http_method.upper()
        self.endpoint = self._ENDPOINT + entity.name
        self._valid_params = ENTITY_ATTR_MAP[entity.name]
        self._data = entity.serialize() if entity else None
        self._url_params = url_params if url_params else None

    @property
    def data(self) -> Union[dict, None]:
        return self._data

    @data.setter
    def data(self, data: Union[Entity, dict]):

        """
        Setter for DriveRequest.data ...

        Accepts either a Drive object 'from entity.drive import Drive',
        a dictionary representing a serialized drive object, or a dictionary
        containing key-value pairs for URL query parameters.
        """

        if isinstance(data, Entity):
            self._data = data.serialize()
        elif isinstance(data, dict):
            self._data = data
        else:
            raise ValueError(f"Property must be set to type 'dict' or 'Entity'")

    @property
    def url_params(self) -> Union[dict, None]:
        return self._url_params

    @url_params.setter
    def url_params(self, params: dict):
        is_get = (self.http_method == EclipseHttpMethod.GET)
        is_valid_params = self._is_valid_params(params)
        if is_get and is_valid_params:
            self._url_params = params

    @property
    def entity(self):
        return self._entity

    def send(self) -> str:

        """
        Send handler for eclipse_request.

        :return: HTTP Response as JSON str, or empty string on failure.
        """

        res = ""
        try:
            if self.http_method == EclipseHttpMethod.GET:
                res = self._get(self.endpoint, self.url_params)
            elif self.http_method == EclipseHttpMethod.POST:
                res = self._post(self.endpoint, self.data)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except json.JSONDecodeError:
            print("Failed to parse JSON response")

        return res

    def _get(self, endpoint: str, params: Union[dict, None]) -> str:

        """
        Generic GET request handler.
        """

        url = urljoin(self._ENDPOINT, endpoint)
        res = requests.get(url, params=params)
        return res.json()

    def _post(self, endpoint: str, data: Union[str, dict]) -> str:

        """
        Generic POST request handler.
        """

        url = urljoin(self._ENDPOINT, endpoint)
        if isinstance(data, str):
            data = json.loads(data)

        res = requests.post(url, json=data)
        return res.json()

    def _is_valid_params(self, params: dict) -> bool:

        """
        Verify if query params are valid for get request.

        Accepts a dictionary intended to represent valid query parameters
        for the Object's endpoint. If endpoint does not support the input params,
        the method will return False.
        """

        params_in = set(params.keys())
        params_valid = set(self._valid_params)
        params_diff = list(params_in.difference(params_valid))

        return len(params_diff) == 0
