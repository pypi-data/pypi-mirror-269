import logging
from .WatrEntity import WatrEntity
from .watrapi import WatrApi

_LOGGER = logging.getLogger(__name__)


class WatrZone(WatrEntity):
    """
    A class representing a sprinkler zone.
    """

    def __init__(self, api: WatrApi, data: dict, system):
        self.__system = system
        super().__init__(data)
        self.__api = api
        # self.__data = {}
        self.__duration = 0
        self.__disabled = False
        self.__is_on = False
        self.__time_remaining = 0
        self.__id = ""
        self.__name = ""
        self.__system_id = system.id
        self.__parse_data(data)

    @property
    def is_on(self) -> bool:
        """
        Returns whether the zone is on.
        :return: Whether the zone is on.
        """
        return self.__is_on

    @property
    def duration(self) -> int:
        """
        Gets the duration of the zone.
        :return: The duration of the zone.
        """
        return self.__duration

    @property
    def disabled(self) -> bool:
        """
        Returns whether the zone is disabled.
        :return: Whether the zone is disabled.
        """
        return self.__disabled

    @property
    def time_remaining(self) -> int:
        """
        Gets the time remaining for the zone.
        :return: The time remaining.
        """
        return self.__time_remaining

    @property
    def api(self) -> WatrApi:
        """
        Returns the API.
        :return: The API.
        """
        return self.__api

    @property
    def system_id(self) -> str:
        """
        Returns the system ID.
        :return: The system ID.
        """
        return self.__system_id

    async def toggle(self) -> None:
        """
        Toggles the zone.
        :return: None
        """
        await self.api.toggle_zone(self.id)
        await self.refresh()
        await self.__system.refresh()

    async def refresh(self) -> None:
        """
        Refreshes the zone data.
        :return: None
        """
        zone_data = await self.api.get_zone(self.id)
        zone_data = zone_data[0]
        if zone_data is None:
            return
        self.__parse_data(zone_data)
        self.emit("update", zone_data)

    def update_data(self, data: dict, override: bool = False):
        """
        Updates the data for the zone.
        :param data: The data to update.
        :param override: Whether to override the existing data.
        :return: None
        """
        self.__parse_data(data)
        self.emit("update", data)

    def __parse_data(self, data: dict) -> None:
        """
        Parses the data from the API.
        :param data: The data to parse.
        :return: None
        """
        if data is list:
            data = data[0]
        self.__data = data
        try:
            self.__duration = data["duration"]
        except TypeError:
            pass
        self.__disabled = data["disabled"]
        self.__is_on = data["isOn"]
        self.__time_remaining = data["timeRemaining"]
        self.__id = data["id"]
        self.__name = data["name"]
