# system imports
from typing import Optional

# user imports
from client.entity import Drive
from _eclipse_request import _EclipseRequest


class _DriveRequest(_EclipseRequest):

    _PARAMS = (
        "file_count",
        "serial_number",
        "storage_total_gb",
        "storage_used_gb",
        "nas_id",
        "delivery_id"
    )

    def __init__(self, http_method: str, drive: Drive, params: Optional[dict] = None):
        super().__init__(http_method, drive, params)
