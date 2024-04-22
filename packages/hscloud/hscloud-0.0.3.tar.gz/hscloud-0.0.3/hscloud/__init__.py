# import json
#
# import requests
#
# from datetime import datetime

# def discover(apiurl, access_token):
#     url = f'{apiurl}/api/device/list'
#     params = {
#         'timestamp': timestamp()
#     }
#
#     response_body = []
#     response = requests.get(url, headers=headers(access_token), params=params)
#
#     if response.status_code == 200:
#         response_body = response.json()
#         if response_body.get("code") == 0:
#             response_body = response_body.get("data")
#
#     return response_body
#
# def status(apiurl, access_token, devicesn):
#     url = f'{apiurl}/api/device/state'
#     params = {
#         "deviceSn": devicesn,
#         'timestamp': timestamp()
#     }
#
#     response_body = {}
#     response = requests.get(url, headers=headers(access_token), params=params)
#
#     if response.status_code == 200:
#         result = response.json()
#         if result.get("code") == 0:
#             response_body = result.get("data").get("state")
#
#     return response_body
#
# def update(apiurl, access_token, devicesn, **kwargs):
#     url = f'{apiurl}/api/device/control'
#     params = {
#         'timestamp': timestamp()
#     }
#
#     response = requests.post(url, headers=headers(access_token), params=params, data=json.dumps(data(devicesn, **kwargs)))
#
#     result = {}
#     if response.status_code == 200:
#         result = response.json()
#
#     return result.get("code") == 0 if True else False
#
# def headers(access_token):
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {access_token}',
#         'UA': 'dreo/'
#     }
#     return headers
#
# def timestamp():
#     return int(datetime.now().timestamp() * 1000)
#
# def data(devicesn, **kwargs):
#     data = {
#         'devicesn': devicesn
#     }
#
#     desired = {}
#     for key, value in kwargs.items():
#         desired.update({key: value})
#
#     data.update({'desired': desired})
#     return data