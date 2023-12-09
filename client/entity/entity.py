import json


class Entity(object):

    def __init__(self):

        self._name = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def serialize(self) -> str:
        """
        Serialize the object to a JSON-formatted string.
        """
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return json.dumps(data, indent=4)
