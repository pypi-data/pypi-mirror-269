import logging
from .entity import Entity
from .watrapi import WatrApi
from .watrsprinklersystem import WatrSprinklerSystem
from .util import first_or_none

_LOGGER = logging.getLogger(__name__)


class WatrSystem(Entity):
    """
    A class representing a collection of sprinkler systems.
    """

    def __init__(self, data: dict, api: WatrApi):
        super().__init__(data)
        self.__api = api
        self.__sprinkler_systems = []

    @property
    def api(self) -> WatrApi:
        """
        Returns the api.
        :return: The api.
        """
        return self.__api

    @property
    def sprinkler_systems(self) -> list[WatrSprinklerSystem]:
        """
        Returns a list of sprinkler systems.
        :return: A list of sprinkler systems.
        """
        return self.__sprinkler_systems

    async def refresh(self) -> None:
        """
        Refreshes the system data.
        :return: None
        """
        system_data = await self.api.get_all_systems()
        if system_data is None:
            return
        for sprinkler_system_data in system_data:
            system = first_or_none(self.__sprinkler_systems,
                                   lambda ss: ss.id == sprinkler_system_data["id"])
            if system:
                await system.refresh()
            else:
                self.__sprinkler_systems.append(WatrSprinklerSystem(sprinkler_system_data, self.api, self))
        self.update_data(
            {
                "data": sprinkler_system_data
            })
