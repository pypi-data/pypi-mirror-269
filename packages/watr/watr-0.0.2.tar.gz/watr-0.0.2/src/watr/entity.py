from collections.abc import Callable

#
# This class is borrowed from: https://github.com/natekspencer/vivintpy/blob/main/vivintpy/entity.py
#
UPDATE = "update"


class Entity:
    """
    A class representing an entity.
    """

    def __init__(self, data: dict):
        self.__data = data
        self._listeners: dict[str, list[Callable]] = {}

    @property
    def data(self) -> dict:
        """
        Returns the raw data of the entity.
        :return: The raw data of the entity.
        """
        return self.__data

    def update_data(self, data: dict, override: bool = False):
        self.__data = data
        self.emit(UPDATE, {"data": data})

    def on(self, event_name: str, callback: Callable) -> Callable:
        listeners = self._listeners.get(event_name, [])
        listeners.append(callback)

        def unsubscribe():
            if callback in listeners:
                listeners.remove(callback)

        return unsubscribe

    def emit(self, event_name: str, data: dict) -> None:
        for listener in self._listeners.get(event_name, []):
            try:
                listener(data)
            except:
                pass
