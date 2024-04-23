import json
import requests as requests


class HttpUtil:
    @staticmethod
    def http_post(url, parameters, headers):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        res = requests.post(url, data=parameters, headers=headers, verify=True)
        if res.status_code != 200:
            raise Exception("Request exception")
        result = json.loads(res.text)
        return result

    @staticmethod
    def http_get(url, parameters, headers):
        res = requests.get(url, data=parameters, headers=headers, verify=True)
        if res.status_code != 200:
            raise Exception(u"Request exception")
        result = json.loads(res.text)
        return result

    @staticmethod
    def http_request(url, method, params, data, body, **kwargs):
        response = requests.request(method, url, params=params, data=data, json=body, **kwargs, verify=True)
        if response.status_code != 200:
            raise Exception(u"Request exception")
        result = response.text
        return result

    @staticmethod
    def http_multipart_request(url, data, files, auth_key):
        headers = {
            'auth-key': auth_key
        }
        response = requests.request("POST", url, headers=headers, data=data, files=files, verify=True)
        result = response.text
        return result
