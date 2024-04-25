from typing import Any, Dict, Final, Optional, Union
import requests

import datetime
import isodate

from washpy.authenticate import authenticate
from washpy.state import State
from washpy.status import *


class DeviceUser:
    """
    device_url: e.g. 'https://192.168.1.251/Devices/000116343328'

    token: a bearer-token, used for authenticating a user with a device at every other XKM API endpoint
    """

    device_url: str
    user: Final[str]
    password: Final[str]
    token: str
    timeout: datetime.timedelta
    last_used: datetime.datetime

    def __init__(self, device_url: str, user: str, password: str) -> None:
        """
        device_url: e.g. 'https://192.168.1.251/Devices/000116343328'

        user: a username

        password: the password of user

        Authenticates the user at the specified machine
        """
        self.user = user
        self.password = password
        self.device_url = device_url
        self.last_used = datetime.datetime.now()
        (self.token, self.timeout) = authenticate(
            self.device_url, self.user, self.password
        )

    def __repr__(self) -> str:
        return (
            f"DeviceUser(device_url='{self.device_url}', "
            f"user='{self.user}', "
            f"password='~~ HIDDEN ~~', "
            f"token='{self.token}', "
            f"timeout={self.timeout.__repr__()}, "
            f"last_used={self.last_used.__repr__()}) "
        )

    def _do_get_request(self, api_endpoint: str) -> Dict[str, Any]:
        """
        queries the api_endpoint, e.g. the `/State` endpoint, of the machine.

        returns: the body of the response as an unpacked json object

        raises: ValueError, if the authentication was unsuccessfull
        """
        url = self.device_url + api_endpoint

        payload = {}
        headers = {"Authorization": f"Bearer {self.token}"}

        now = self.refresh_authentication()
        response = requests.request(
            "GET", url, headers=headers, data=payload, verify=False
        )

        if response.status_code != 200:
            raise ValueError(f"Unable to authenticate: got HTTP response {response}")
        self.last_used = now
        return response.json()

    def refresh_authentication(self) -> datetime.datetime:
        """
        if self.token is only valid for less then 10 seconds
        or if it is invalid,
        refresh it.

        returns: the point in time at which the check has happened
        """
        now = datetime.datetime.now()
        token_valid_date = self.last_used + self.timeout
        if now > token_valid_date - datetime.timedelta(seconds=10):
            (self.token, self.timeout) = authenticate(
                self.device_url, self.user, self.password
            )
            self.last_used = now
        return now

    def get_State(self) -> State:
        """
        queries the `/State` endpoint.

        returns: a complete state of the machine

        raises: ValueError, if the authentication was unsuccessfull
        """
        return State(**self._do_get_request("/State"))
