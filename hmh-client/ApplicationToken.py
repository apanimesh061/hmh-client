import requests
from requests import exceptions
import cPickle
import sys


class Object(object):
    def __init__(self, **response):
        for k, v in response.iteritems():
            if isinstance(v, dict):
                self.__dict__[k] = Object(**v)
            else:
                self.__dict__[k] = v


class Credentials(object):
    def __init__(self, request_url, hmh_api_key, client_id, grant_type, username, password, refresh_token=None):
        assert isinstance(request_url, (str, unicode)), request_url
        assert isinstance(hmh_api_key, (str, unicode)), hmh_api_key
        assert isinstance(client_id, (str, unicode)), client_id
        assert isinstance(grant_type, (str, unicode)), grant_type
        assert isinstance(username, (str, unicode)), username
        assert isinstance(password, (str, unicode)), password
        self.request_url = request_url
        self.hmh_api_key = hmh_api_key
        self.client_id = client_id
        self.grant_type = grant_type
        self.username = username
        self.password = password
        if refresh_token:
            assert isinstance(refresh_token, (str, unicode)), refresh_token
        self.refresh_token = refresh_token

    def get_response(self):
        values = {
            "client_id": self.client_id,
            "grant_type": self.grant_type,
            "username": self.username,
            "password": self.password,
        }
        if self.grant_type == "refresh_token" and self.refresh_token:
            values["refresh_token"] = self.refresh_token
            from pprint import pprint
            pprint(values)
        try:
            r = requests.post(self.request_url, values)
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    @staticmethod
    def to_object(response):
        return Object(**response)

    @staticmethod
    def save_as(tokens, filename):
        return cPickle.dump(tokens, open(filename, "wb"))
