from .helpers import Helpers

class HsCloud:

    def __init__(self, username=None, password=None):
        super().__init__()
        self.username = username
        self.password = password
        self.access_token = None

    def login(self) -> bool:
        response = Helpers.call_api("/api/oauth/login", "post", Helpers.headers(), Helpers.params(), Helpers.login_body(self.username, self.password))
        if response[0]:
            self.access_token = response[1].get("access_token")
        return response[0]

    def devices(self) -> tuple:
        return Helpers.call_api("/api/device/list", "get", Helpers.headers(self.access_token), Helpers.params())[1]

    def status(self, devicesn) -> tuple:
        return Helpers.call_api("/api/device/state", "get", Helpers.headers(self.access_token), Helpers.params(devicesn))[1]

    def update(self, devicesn, **kwargs) -> bool:
        return Helpers.call_api("/api/device/control", "post", Helpers.headers(self.access_token), Helpers.params(), Helpers.update_body(devicesn, **kwargs))[0]