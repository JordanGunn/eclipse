# system imports
from typing import Optional

# user imports
import _eclipse_http_method
from client.entity.drive import Drive
from _drive_request import _DriveRequest


class EclipseRequest:
    @staticmethod
    def create_request(http_method: str, eclipse_entity: Optional[object] = None):
        """
        Factory method to create different types of requests based on the object type.

        :param http_method: The HTTP method for the request.
        :param eclipse_entity: The object for which the request is being made.
        :return: An instance of a specific request type.
        """

        # make sure http_method is valid
        if http_method not in _eclipse_http_method.LIST:
            raise ValueError(f"Unsupported HTTP request type: '{http_method}'")

        if isinstance(eclipse_entity, Drive):
            return _DriveRequest(http_method, eclipse_entity)
        else:
            # You can add more conditions for different types of objects
            raise ValueError(f"Unsupported object type: {eclipse_entity.__class__.__name__}")


def main():

    drv = Drive(1, 2)
    drv_req = EclipseRequest.create_request("GET", drv)
    drv_req.send()


if __name__ == "__main__":
    main()
