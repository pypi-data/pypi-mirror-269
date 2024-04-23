import json
import requests
from datetime import datetime
import logging
from typing import NamedTuple, Optional, Union

logger = logging.getLogger(__name__)

API_BASE_URL = 'http://10.10.20.109:2070'
API_RATE_LIMIT = 30
API_TIMEOUT = 8

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
    def timestamp():
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def call_api(api: str, method: str, headers: Optional[dict] = None, params: Optional[dict] = None, json_body: Optional[dict] = None) -> tuple:
        """Make API calls by passing endpoint, header and body."""
        response = None
        result = None
        status_code = None

        try:
            if method.lower() == 'get':
                response = requests.get(API_BASE_URL + api, headers=headers, params=params, timeout=API_TIMEOUT)

            elif method.lower() == 'post':
                response = requests.post(API_BASE_URL + api, headers=headers, params=params, json=json_body, timeout=API_TIMEOUT)

        except requests.exceptions.RequestException as e:
            logger.debug(e)
        except Exception as e:  # pylint: disable=broad-except
            logger.debug(e)
        else:
            if response.status_code == 200:
                response_body = response.json()
                if response_body.get("code") == 0:
                    status_code = response_body.get("code")
                    result = response_body.get("data")
        return status_code, result