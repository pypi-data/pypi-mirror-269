from .helpers import Helpers

class HsCloud:

    def __init__(self, username=None, password=None):
        super().__init__()
        self.username = username
        self.password = password

    def login(self) -> tuple:
        return Helpers.call_api("/api/oauth/login", "post", Helpers.headers(), Helpers.params(), Helpers.login_body(self.username, self.password))

    def devices(self, access_token) -> tuple:
        return Helpers.call_api("/api/device/list", "get", Helpers.headers(access_token), Helpers.params())

    def status(self, access_token, devicesn) -> tuple:
        return Helpers.call_api("/api/device/state", "get", Helpers.headers(access_token), Helpers.params(devicesn))

    def update(self, access_token, devicesn, **kwargs) -> bool:
        response = Helpers.call_api("/api/device/control", "post", Helpers.headers(access_token), Helpers.params(), Helpers.update_body(devicesn, **kwargs))
        return response[0]