from .entity import Entity


class WatrEntity(Entity):
    @property
    def id(self) -> str:
        """
            Returns the id of the entity.
            :return: The id of the entity.
            """
        return self.data["id"]

    @property
    def name(self) -> str:
        """
            Returns the name of the entity.
            :return: The name of the entity.
            """
        return self.data["name"]