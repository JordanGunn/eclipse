# system imports
import json
import requests
from typing import Union, Optional
from urllib.parse import urljoin

# user imports
from client.entity.entity import Entity
from eclipse_config import NetworkConfig
from client.entity.entity_attrs import ENTITY_ATTR_MAP


class _EclipseHttpMethod:

    """Valid http methods enabled for eclipse"""

    GET = "GET"
    POST = "POST"
    LIST = [GET, POST]


class EclipseRequest:

    """EclipseRequest class. Prepares and handles send/recv of eclipse HTTP requests."""

    _PORT = NetworkConfig.PORT.DEFAULT
    _HOST = NetworkConfig.HOST.DEFAULT
    _ENDPOINT = f"http://{_HOST}:{str(_PORT)}/api/"

    def __init__(self, http_method: str, entities: Union[Entity, list[Entity]], url_params: Optional[dict] = None):

        """
        Initialize EclipseRequest object.

        Constructor has one optional argument 'url_params'. The url_params must be passed as
        a dictionary containing valid url query parameters for the entity associated with it.

        GET request for the Drive entity using 'id' and 'serial_number' query parameters:
        >>> from client.entity.drive import Drive
        >>> params = {"id": 1, "serial_number": "DEADBEEF"}
        >>> drive = Drive()
        >>> erq = EclipseRequest("GET", drive, params)

        POST request for multiple drive entities:
        >>> from client.entity.drive import Drive
        >>> drives = [Drive(nas_id=1, delivery_id=1), Drive(nas_id=2, delivery_id=1), Drive(nas_id=3, delivery_id=1)]
        >>> erq = EclipseRequest("POST", drives, params=None)


        :param http_method: A valid HTTP request method (e.g. 'GET', 'Get', 'gEt').
        :param entities: One or more objects that intherit from the Entity base class (e.g. Drive object)
        :raises ValueError:
        """

        # property initialization
        self._data = None
        self._endpoint = ""
        self._entities = None
        self._valid_params = None

        # Validate http method
        if http_method.upper() not in _EclipseHttpMethod.LIST:
            raise ValueError(f"Unsupported HTTP method: {http_method}")
        else:
            self.http_method = http_method.upper()

        # call the entities setter
        self.entities = entities

        # validate url params
        if url_params and self._is_valid_params(url_params):
            self._url_params = url_params
        else:
            self._url_params = None

    @property
    def data(self) -> str:

        """Get EclipseRequest 'data' property."""

        return self._data

    @property
    def url_params(self) -> Union[dict, None]:

        """Get EclipseRequest 'url_params' property."""

        return self._url_params

    @url_params.setter
    def url_params(self, params: dict):

        """
        Set the EclipseRequest 'url_params' property.

        Sets the url params property in the event that the EclipseRequest
        was initialized for the 'GET' http method.

        Also note that the argument params must contain
        valid query parameters for the derived Entity
        object. If params argument contains invalid
        query parameters, method will raise a ValueError.

        :param params: A dictionary containing key-value query params.
        :raises ValueError: Failure to pass valid url query params.
        """

        is_get = (self.http_method == _EclipseHttpMethod.GET)
        if is_get:
            if self._is_valid_params(params):
                self._url_params = params
            else:
                raise ValueError(
                    f"Invalid query parameters: {params.keys()}"
                )
        else:
            self._url_params = None

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def entities(self) -> list[Entity]:

        """Get EclipseRequest 'entity' property."""

        return self._entities

    @entities.setter
    def entities(self, entities: Union[Entity, list[Entity]]):

        # place single entity in a list to have consistent logic
        if isinstance(entities, Entity):
            self._entities = [entities]
        # make sure all entities are the same type
        elif all(isinstance(entity, type(entities[0])) for entity in self.entities):
            self._entities = entities
        # if entities are not the same subtype, raise exception.
        else:
            raise ValueError("All entities must be instances of the same subclass of Entity")

        e_ref = self._entities[0]
        self._endpoint = self._ENDPOINT + e_ref.name + "/"
        self._valid_params = ENTITY_ATTR_MAP[e_ref.name]
        self._data = [e.serialize(as_dict=True) for e in self.entities]

    def send(self) -> Union[dict, None]:

        """
        Send handler for eclipse_request.

        :return: HTTP Response as JSON str, or empty string on failure.
        """

        res = None
        try:
            if self.http_method == _EclipseHttpMethod.GET:
                res = self._get(self.endpoint, self.url_params)
            elif self.http_method == _EclipseHttpMethod.POST:
                res = self._post(self.endpoint, self.data)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except json.JSONDecodeError:
            print("Failed to parse JSON response")

        return res

    def _get(self, endpoint: str, params: Optional[dict]) -> str:

        """
        Generic GET request handler.

        :param endpoint: API endpoint.
        :param params: A valid url query params dictionary.
        :return:
        """

        url = urljoin(self._ENDPOINT, endpoint)
        res = requests.get(url, params=params)
        return res.json()

    def _post(self, endpoint: str, data: Union[str, dict]) -> str:

        """
        Generic POST request handler.

        :param endpoint: API endpoint.
        :param data: A valid url query params dictionary.
        :return:
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

        if not params:
            return False

        params_in = set(params.keys())
        params_valid = set(self._valid_params)
        params_diff = list(params_in.difference(params_valid))

        return len(params_diff) == 0
