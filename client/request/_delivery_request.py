# system imports
from typing import Optional

# user imports
from client.entity import Delivery
from _eclipse_request import _EclipseRequest


class _DeliveryRequest(_EclipseRequest):

    _PARAMS = (
        "receiver_name",
        "comments",
        "timestamp"
    )

    def __init__(self, http_method: str, delivery: Delivery = None, params: Optional[dict] = None):
        super().__init__(http_method, delivery, params)
