import requests
import hashlib
import json
# import urllib
import urllib.parse
from collections import OrderedDict


DEFAULT_GROUP_API_BASE = "https://api.ok.ru/fb.do"


class GroupApi:
    def __init__(self, config):
        self.config = config

    def make_post(self, content):
        # body = urllib.parse.urlencode(self.build_url(content))
        body = self.build_url(content)
        # print("Request body")
        print(body)
        url = DEFAULT_GROUP_API_BASE
        result = requests.post(url, data=body, headers={
            "content-type": "application/x-www-form-urlencoded"
        })
        print(result.content)
        if result.status_code != 200:
            raise RuntimeError("Failed to post media!")

    def build_url(self, attachment):
        # print(json.dumps(attachment))
        target = {
            "application_key": self.config.application_key,
            "access_token": self.config.access_token,
            "type": "GROUP_THEME",
            "gid": self.config.group_id,
            "format": "json",
            "method": "mediatopic.post",
            "attachment": json.dumps(attachment)
        }
        sig = GroupApi.calc_sig(target, self.config.session_secret_key)
        target["sig"] = sig
        return target

    @staticmethod
    def calc_sig(data, secret):
        reserved = ["session_key", "access_token"]
        result = OrderedDict()
        for key in sorted(data.keys()):
            if key not in reserved:
                result[key] = data[key]
        result_string = []
        for key, value in result.items():
            result_string.append(f"{key}={value}")
        result_string.append(secret)
        hasher = hashlib.md5()
        hasher.update("".join(result_string).encode("utf8"))
        return hasher.hexdigest()
