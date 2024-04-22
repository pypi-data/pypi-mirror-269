import json

from hscloud.helpers import Helpers
import hashlib

class HsCloud:

    def __init__(self, username=None, password=None):
        super().__init__()
        self.username = username
        self.password = password
        self.access_token = None

    def login(self) -> bool:
        params = {
            'timestamp': Helpers.timestamp()
        }

        json_body = {
            "client_id": "89ef537b2202481aaaf9077068bcb0c9",
            "client_secret": "41b20a1f60e9499e89c8646c31f93ea1",
            "grant_type": "openapi",
            "scope": "all",
            "email": self.username,
            "password": hashlib.md5(self.password.encode('utf-8')).hexdigest()
        }

        response = Helpers.call_api("/api/oauth/login", "post", Helpers.headers(), params, json_body)
        is_falg = False
        if ( response[0] == 0 ):
            self.access_token = response[1].get("access_token")
            is_falg = True
        return is_falg

    def devices(self):
        params = {
            'timestamp': Helpers.timestamp()
        }

        return Helpers.call_api("/api/device/list", "get", Helpers.headers(self.access_token), params)

    def status(self, access_token=None, deviceSn=None):
        params = {
            "deviceSn": self.deviceSn,
            'timestamp': Helpers.timestamp()
        }

        return Helpers.call_api("/api/device/state", "get", Helpers.headers(self.access_token), params)

    def update(self) -> bool:
        return True