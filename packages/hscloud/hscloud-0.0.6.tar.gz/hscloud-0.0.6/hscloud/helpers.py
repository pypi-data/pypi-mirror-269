import json
import requests
from datetime import datetime
import logging
from typing import NamedTuple, Optional, Union

logger = logging.getLogger(__name__)

URL = 'http://10.10.20.109:2070'
TIMEOUT = 8

class Helpers:

    @staticmethod
    def headers(access_token=None):
        headers = None
        if access_token is not None:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}',
                'UA': 'dreo/'
            }
        else:
            headers = {
                'Content-Type': 'application/json',
                'UA': 'dreo/'
            }
        return headers

    @staticmethod
    def params(devicesn=None):
        params = None
        if devicesn is not None:
            params = {
                'deviceSn': devicesn,
                'timestamp': Helpers.timestamp()
            }
        else:
            params = {
                'timestamp': Helpers.timestamp()
            }
        return params

    @staticmethod
    def login_body(username=None, password=None):
        body = {
                "client_id": "89ef537b2202481aaaf9077068bcb0c9",
                "client_secret": "41b20a1f60e9499e89c8646c31f93ea1",
                "grant_type": "openapi",
                "scope": "all",
                "email": username,
                "password": password
            }
        return body

    @staticmethod
    def update_body(devicesn, **kwargs):
        data = {
            'devicesn': devicesn
        }

        desired = {}
        for key, value in kwargs.items():
            desired.update({key: value})

        data.update({'desired': desired})
        return data

    @staticmethod
    def timestamp():
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def call_api(api: str, method: str, headers: Optional[dict] = None, params: Optional[dict] = None, json_body: Optional[dict] = None) -> tuple:
        response = None
        response_code = False
        response_data = None

        try:
            if method.lower() == 'get':
                response = requests.get(URL + api, headers=headers, params=params, timeout=TIMEOUT)

            elif method.lower() == 'post':
                response = requests.post(URL + api, headers=headers, params=params, json=json_body, timeout=TIMEOUT)

        except requests.exceptions.RequestException as e:
            logger.debug(e)
        except Exception as e:
            logger.debug(e)
        else:
            if response.status_code == 200:
                response_body = response.json()
                if response_body.get("code") == 0:
                    response_code = True
                    response_data = response_body.get("data")
        return response_code, response_data