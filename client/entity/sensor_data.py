import os
from typing import Optional

from .entity import Entity
from .entity_attrs import EntityName


GB_CONVERT = (1024 * 1024 * 1024)


class SensorData(Entity):

    def __init__(self, nas_id: int, delivery_id: int, file_path: Optional[str] = ""):
        super().__init__()
        Entity.name = EntityName.NASBOX

        self.nas_id_ = nas_id
        self.delivery_id_ = delivery_id

        if file_path:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"No such path: '{file_path}'")
            self.file_path_ = file_path
            self.file_name_ = os.path.basename(file_path)
            self.file_size_ = os.path.getsize(file_path) / GB_CONVERT
        else:
            self.file_name_ = ""
            self.file_size_ = float("nan")

    @property
    def nas_id(self) -> int:
        return self.nas_id_

    @property
    def delivery_id(self) -> int:
        return self.delivery_id_

    @property
    def file_name(self) -> str:
        return self.file_name_

    @property
    def file_size(self) -> float:
        return self.file_size_

    @property
    def file_path(self) -> str:
        return self.file_path_

    @file_path.setter
    def file_path(self, file_path: str):
        if os.path.exists(file_path):
            self.file_path_ = file_path
            self.file_name_ = os.path.basename(file_path)
            self.file_size_ = os.path.getsize(file_path) / GB_CONVERT
        else:
            raise FileNotFoundError(f"No such path: '{file_path}'")
