import requests
import sys
from requests import exceptions


class IdentityConn(object):
    base_url = None
    info_uri = None
    role_id = None
    response = None

    def __init__(self, access_token, api_key, base_url, info_uri, role_id=None):
        self.base_url = base_url
        self.info_uri = info_uri
        self._set_access_token(access_token)
        self._set_api_key(api_key)
        if role_id:
            self.role_id = role_id

    def _set_access_token(self, access_token):
        assert isinstance(access_token, (str, unicode)), access_token
        self.access_token = access_token

    def _set_api_key(self, api_key):
        assert isinstance(api_key, (str, unicode)), api_key
        self.api_key = api_key

    def set_request(self):
        headers = {
            "Vnd-HMH-Api-Key": self.api_key,
            "Authorization": self.access_token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if self.role_id:
            current_url = self.base_url + self.info_uri + "/" + self.role_id
        else:
            current_url = self.base_url + self.info_uri
        try:
            r = requests.get(url=current_url, headers=headers)
            r.raise_for_status()
            self.response = r
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def get_response(self):
        return self.response.json()


class Identity(object):
    response = None

    def __init__(self):
        self.access_token = None
        self.api_key = None

    def set_access_token(self, access_token):
        assert isinstance(access_token, (str, unicode)), access_token
        self.access_token = access_token

    def set_api_key(self, api_key):
        assert isinstance(api_key, (str, unicode)), api_key
        self.api_key = api_key

    def get_all(self, base_url, info_uri):
        print "Requesting all", self.__class__.__name__, "type roles"
        req = IdentityConn(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri)
        req.set_request()
        self.response = req.get_response()

    def get_by_id(self, base_url, info_uri, role_id):
        print "Requesting", self.__class__.__name__, "role having refID", role_id
        req = IdentityConn(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                           role_id=role_id)
        req.set_request()
        self.response = req.get_response()

    def get_response(self):
        return self.response
