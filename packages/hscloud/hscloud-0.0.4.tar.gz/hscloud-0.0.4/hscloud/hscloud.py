import json

from hscloud.helpers import Helpers
import hashlib

class HsCloud:

    def __init__(self, username=None, password=None):
        super().__init__()
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None

    def login(self) -> bool:
        response = Helpers.requests("/api/oauth/login", "post", Helpers.headers(), Helpers.params(), Helpers.login_body(self.username, self.password))
        if response[0] == 0:
            self.access_token = response[1].get("access_token")
            self.refresh_token = response[1].get("refresh_token")
            return True
        else:
            return False

    def get_devices(self) -> tuple:
        response = Helpers.requests("/api/device/list", "get", Helpers.headers(self.access_token), Helpers.params())
        return response[1]

    def get_status(self, devicesn) -> tuple:
        response = Helpers.requests("/api/device/state", "get", Helpers.headers(self.access_token), Helpers.params(devicesn))
        return response[1]

    def update(self, devicesn, **kwargs) -> bool:
        response = Helpers.requests("/api/device/control", "post", Helpers.headers(self.access_token), Helpers.params(), Helpers.update_body(devicesn, **kwargs))
        return response[0] == 0 if True else False