import logging
import aiohttp
import json
import ssl
import certifi
from aiohttp.client import _RequestContextManager
from collections.abc import Callable
from .watrexceptions import WatrApiInvalidTokenException

API_ENDPOINT = "https://watr-dev-webapp.peasenet.com/api/v1"
API_ACCOUNT_LOGIN = "account/login"
API_ACCOUNT_VALIDATE = "account/validate"
API_ACCOUNT_REFRESH = "account/refresh"

API_SYSTEM_GET_ALL = "system/systems"

_LOGGER = logging.getLogger(__name__)


class WatrApi:
    """
    A class to interact with the Watr API.
    """

    def __init__(self,
                 username: str | None = None,
                 password: str | None = None,
                 client_session: aiohttp.ClientSession | None = None,
                 access_token: str | None = None,
                 refresh_token: str | None = None):
        self.__username = username
        self.__password = password
        self.__client_session = client_session or self.__get_client_session()
        self.__access_token = access_token
        self.__refresh_token = refresh_token
        self._listeners: dict[str, list[Callable]] = {}

    async def authenticate(self, remember: bool = False) -> bool:
        """
        Authenticates the user with the given username and password.
        :param remember: Whether to remember the user.
        :return: True if the authentication was successful, False otherwise.
        """
        if self.__access_token and self.__refresh_token:
            if await self.is_valid_token():
                _LOGGER.debug("Token is valid")
                return True
            else:
                _LOGGER.debug("Token is invalid")
                return False
        if not self.__username or not self.__password:
            _LOGGER.error("Username or password not provided")
            return False
        data = {
            "Email": self.__username,
            "Password": self.__password,
            "RememberMe": remember
        }
        resp = await self.__post(API_ACCOUNT_LOGIN, data)
        if resp:
            self.__access_token = resp["tokens"]["accessToken"]
            self.__refresh_token = resp["tokens"]["refreshToken"]
            _LOGGER.debug("Authentication successful")
            data = {
                "accessToken": self.__access_token,
                "refreshToken": self.__refresh_token
            }
            self.emit("token_refresh", data)
            return True
        else:
            _LOGGER.error("Authentication failed")
            return False

    async def is_valid_token(self) -> bool:
        """
        Checks if the current access token is valid.
        :return: True if the token is valid, False otherwise.
        """
        if not self.__access_token:
            return False
        resp = await self.__get(API_ACCOUNT_VALIDATE)
        return True if resp["success"] else False

    async def refresh_token(self) -> bool:
        """
        Refreshes the access token using the refresh token.
        :return: True if the token was refreshed, False otherwise.
        """
        data = {
            "refreshToken": self.__refresh_token,
            "accessToken": self.__access_token
        }
        resp = await self.__post(API_ACCOUNT_REFRESH, data)
        if resp and resp["success"]:
            self.__access_token = resp["newTokens"]["accessToken"]
            self.__refresh_token = resp["newTokens"]["refreshToken"]
            _LOGGER.debug("Token refreshed")
            data = {
                "accessToken": self.__access_token,
                "refreshToken": self.__refresh_token
            }
            self.emit("token_refresh", data)
            return True
        else:
            _LOGGER.error("Token refresh failed")
            return False

    # === System API ===
    async def get_all_systems(self) -> dict | None:
        """
        Gets all systems associated with the authenticated user.
        :return: A dictionary containing the systems.
        """
        return await self.__get(API_SYSTEM_GET_ALL)

    async def toggle_system(self, system_id: str) -> None:
        """
        Toggles the system with the given system_id.
        :param system_id: The system_id of the system to toggle.
        :return: None
        """
        path = f"system/{system_id}/toggle"
        await self.__post(path)

    async def get_system(self, system_id: str) -> dict | None:
        """
        Gets the system with the given system_id.
        :param system_id: The system_id of the system to get.
        :return: None
        """
        path = f"system/{system_id}"
        return await self.__get(path)

    # === End System API ===

    # === Zone API ===
    async def get_zone(self, zone_id: str) -> dict | None:
        """
        Gets the zone with the given zone_id.
        :param zone_id: The zone_id of the zone to get.
        :return: None
        """
        path = f"zone/{zone_id}"
        return await self.__get(path)

    async def toggle_zone(self, zone_id: str) -> None:
        """
        Toggles the zone with the given zone_id.
        :param zone_id: The zone_id of the zone to toggle.
        :return: None
        """
        path = f"zone/{zone_id}/toggle"
        await self.__post(path)

    # === End Zone API ===

    async def disconnect(self):
        """
        Closes the client session.
        :return: 
        """
        _LOGGER.debug("Disconnecting")
        await self.__client_session.close()

    async def __get(self, path: str, params: dict | None = None) -> dict | None:
        """
        Sends a GET request to the given path.
        :param path: The path to send the request to.
        :param params: The parameters to send with the request.
        :return: A dictionary containing the response, or None if the request failed.
        """
        url = f"{API_ENDPOINT}/{path}"
        resp = await self.__call(self.__client_session.get, url, params=params)
        return resp

    async def __post(self, path: str, data: dict | None = None) -> dict | None:
        """
        Sends a POST request to the given path.
        :param path: The path to send the request to.
        :param data: The data to send with the request.
        :return: A dictionary containing the response, or None if the request failed.
        """
        url = f"{API_ENDPOINT}/{path}"
        headers = {
            "Content-Type": "application/json"
        }
        resp = await self.__call(self.__client_session.post, url, data=json.dumps(data), headers=headers)
        return resp

    async def __call(self, method: Callable[..., _RequestContextManager],
                     path: str,
                     headers: dict | None = None,
                     params: dict | None = None,
                     data: str | None = None) -> dict | None:
        """
        Calls the given method with the given parameters.
        If the request fails with a 401 status code, it will attempt to refresh the token and try again.
        :param method: The method to call.
        :param path: The path to send the request to.
        :param headers: The headers to send with the request.
        :param params: The parameters to send with the request.
        :param data: The data to send with the request.
        :return: A dictionary containing the response, or None if the request failed.
        """
        try:
            # add Authorization: Bearer header
            headers = headers or {}
            if self.__access_token:
                headers["Authorization"] = f"Bearer {self.__access_token}"
            resp = await method(
                path,
                headers=headers,
                params=params,
                data=data
            )
            async with resp:
                if resp.status == 401 and path != API_ACCOUNT_REFRESH:
                    # Re-authenticate and try again
                    _LOGGER.debug("Refreshing token")
                    await self.refresh_token()
                    resp = await method(
                        path,
                        headers=headers,
                        params=params,
                        data=data
                    )
                if resp.status == 401 and path == API_ACCOUNT_REFRESH:
                    raise WatrApiInvalidTokenException("Failed to refresh token")
                _LOGGER.debug(f"Response: {resp.status}")
                if resp.content_type == "application/json":
                    return await resp.json()
                else:
                    data = await resp.text()
                    return json.loads(data)
        except Exception as e:
            logging.error(f"Error: {e}")
        return None

    def __get_client_session(self) -> aiohttp.ClientSession:
        """
        Returns a new aiohttp client session.
        :return: A new aiohttp client session.
        """
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where()
        )
        connector = aiohttp.TCPConnector(enable_cleanup_closed=True, ssl=ssl_context)
        return aiohttp.ClientSession(connector=connector)

    def on(self, event_name: str, callback: Callable) -> Callable:
        """
        Adds a listener for the given event.
        :param event_name: The name of the event to listen for.
        :param callback: The callback to call when the event is emitted.
        :return: A function to unsubscribe from the event.
        """
        listeners = self._listeners.get(event_name, [])
        listeners.append(callback)
        _LOGGER.debug(f"Added listener for {event_name}")

        def unsubscribe():
            if callback in listeners:
                listeners.remove(callback)

        self._listeners[event_name] = listeners
        return unsubscribe

    def emit(self, event_name: str, data: dict) -> None:
        """
        Emits an event with the given data.
        :param event_name: The name of the event to emit.
        :param data: The data to emit with the event.
        :return: None
        """
        _LOGGER.debug(f"Emitting event: {event_name} with data: {data}")
        for listener in self._listeners.get(event_name, []):
            try:
                _LOGGER.debug(f"Calling listener for {event_name}")
                listener(data)
            except Exception as e:
                _LOGGER.error(f"Error emitting event: {event_name} - {e}")
                pass
