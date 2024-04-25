import logging
from .WatrEntity import WatrEntity
from .watrapi import WatrApi
from .watrzone import WatrZone
from .util import first_or_none

_LOGGER = logging.getLogger(__name__)


class WatrSprinklerSystem(WatrEntity):
    """
    A class representing a sprinkler system which contains a collection of zones.
    """

    def __init__(self, data: dict, api: WatrApi, system):
        self.__system = system
        super().__init__(data)
        self.__api = api
        self.__zones = []
        self.__events = []
        self.__schedules = []
        self.__parse_data(data)

    def __repr__(self):
        return f"{self.data}"

    @property
    def zones(self) -> list[WatrZone]:
        """
        Returns the zones for the system.
        :return: the zones for the system.
        """
        return self.__zones

    @property
    def events(self) -> list | None:
        """
        Returns the events for the system.
        :return: The events for the system.
        """
        return self.data["events"]

    @property
    def zip_code(self) -> str:
        """
        Returns the zip code for the system.
        :return: The zip code for the system.
        """
        return self.data["zipCode"]

    @property
    def enabled(self) -> bool:
        """
        Returns whether the system is enabled.
        :return: Whether the system is enabled.
        """
        return self.data["enabled"]

    @property
    def schedules(self) -> list | None:
        """
        Returns the schedules for the system.
        :return: The schedules for the system.
        """
        return self.data["schedules"]

    @property
    def weather_check(self) -> bool:
        """
        Returns whether the system has weather check enabled.
        :return: 
        """
        return self.data["weatherCheck"]

    async def toggle(self) -> None:
        """
        Toggles the system.
        :return: None
        """
        await self.__api.toggle_system(self.id)
        await self.refresh()

    async def refresh(self) -> None:
        """
        Refreshes the system data.
        :return: None
        """
        system_data = await self.__api.get_system(self.id)
        if system_data is None:
            return
        self.update_data(system_data)
        for z in system_data["zones"]:
            # if the zone is not in the list of zones, add it
            _zone = first_or_none(self.zones, lambda _zz: _zz.id == z["id"])
            if not _zone:
                self.__zones.append(WatrZone(self.__api, z, self))
            else:
                _zone.update_data(z)

    def __parse_data(self, data: dict) -> None:
        if data is None:
            _LOGGER.error("No data provided to parse")
            return
        # self.__zones = data["zones"]
        for z in data["zones"]:
            self.__zones.append(WatrZone(self.__api, z, self))
        self.__events = data["events"]
        self.__schedules = data["schedules"]
