# system imports
import json
import requests
from typing import Union, Optional
from urllib.parse import urljoin

# user imports
from eclipse_entity.drive import Drive
from eclipse_table import EclipseTable


class EclipseHttpMethod:

    """Enabled HTTP methods for Eclipse."""

    GET = "GET"
    POST = "POST"
    LIST = [GET, POST]


class EclipseRequestFactory:
    @staticmethod
    def create_request(http_method: str, eclipse_entity: Optional[object] = None):
        """
        Factory method to create different types of requests based on the object type.

        :param http_method: The HTTP method for the request.
        :param eclipse_entity: The object for which the request is being made.
        :return: An instance of a specific request type.
        """

        # make sure http_method is valid
        if http_method not in EclipseHttpMethod.LIST:
            raise ValueError(f"Unsupported HTTP request type: '{http_method}'")

        if isinstance(eclipse_entity, Drive):
            return _DriveRequest(http_method, eclipse_entity)
        else:
            # You can add more conditions for different types of objects
            raise ValueError(f"Unsupported object type: {eclipse_entity.__class__.__name__}")


class _EclipseRequest:

    """Private class. Acts as parent to various Eclipse Entities"""

    _PARAMS = tuple()
    _ENDPOINT = "/eclipse/api/"

    def __init__(self, http_method: str):

        if http_method.upper() not in EclipseHttpMethod.LIST:
            raise ValueError(f"Unsupported HTTP method: {http_method}")

        self._data = None
        self.endpoint = self._ENDPOINT
        self.http_method = http_method.upper()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: Union[Drive, dict]):

        """
        Setter for DriveRequest.data ...

        Accepts either a Drive object 'from eclipse_entity.drive import Drive',
        a dictionary representing a serialized drive object, or a dictionary
        containing key-value pairs for URL query parameters.
        """

        if isinstance(data, Drive):
            self._data = data.serialize()
        if isinstance(data, dict):
            is_get = (self.http_method == EclipseHttpMethod.GET)
            invalid_params = not self.is_valid_params(data)

            if is_get and invalid_params:
                raise ValueError(f"Invalid URL query params for endpoint: {self.endpoint}")

            self._data = data

    def send(self) -> str:

        """
        Send handler for EclipseRequest.

        :return: HTTP Response as JSON str, or empty string on failure.
        """

        res = ""
        try:
            if self.http_method == EclipseHttpMethod.GET:
                res = self._get(self.endpoint, self.data)
            elif self.http_method == EclipseHttpMethod.POST:
                res = self._post(self.endpoint, self.data)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except json.JSONDecodeError:
            print("Failed to parse JSON response")

        return res

    def _get(self, endpoint: str, params: dict = None) -> str:

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

    def is_valid_params(self, params: dict) -> bool:

        """
        Verify if query params are valid for get request.

        Accepts a dictionary intended to represent valid query parameters
        for the Object's endpoint. If endpoint does not support the input params,
        the method will return False.
        """

        params_in = set(params.keys())
        params_valid = set(self._PARAMS)
        params_diff = list(params_in.difference(params_valid))

        return len(params_diff) == 0


class _DriveRequest(_EclipseRequest):

    _DRIVE_ENDPOINT = EclipseTable.DRIVE + "/"
    _PARAMS = ("file_count", "serial_number", "storage_total_gb", "storage_used_gb", "nas_id", "delivery_id")

    def __init__(self, http_method: str, drive: Optional[Drive] = None):
        super().__init__(http_method)

        self.drive = drive
        self.endpoint = urljoin(_EclipseRequest._ENDPOINT, self._DRIVE_ENDPOINT)
        if drive and self.http_method == EclipseHttpMethod.POST:
            self._data = drive.serialize()
        else:
            self._data = None


def main():

    drv = Drive(1, 2)
    req = EclipseRequestFactory.create_request("POST", drv)



if __name__ == "__main__":
    main()













