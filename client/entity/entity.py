import json
from typing import Union


class Entity(object):

    def __init__(self):

        self._name = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def serialize(self, as_dict=False) -> Union[str, dict]:
        """
        Serialize the object to a JSON-formatted string.
        """
        data = {k[:-1]: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return data if as_dict else json.dumps(data, indent=4)
