import requests
from requests import exceptions
import sys
import json


class TagsConn(object):
    base_url = None
    info_uri = None
    role_id = None
    response = None

    def __init__(self, access_token, api_key, base_url, info_uri, tag_id=None, tag_name=None, delete_tag=False):
        self.base_url = base_url
        self.info_uri = info_uri
        self._set_access_token(access_token)
        self._set_api_key(api_key)
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.delete_tag = delete_tag
        self.headers = {
            "Vnd-HMH-Api-Key": self.api_key,
            "Authorization": self.access_token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _set_access_token(self, access_token):
        assert isinstance(access_token, (str, unicode)), access_token
        self.access_token = access_token

    def _set_api_key(self, api_key):
        assert isinstance(api_key, (str, unicode)), api_key
        self.api_key = api_key

    def _delete_request(self):
        try:
            request_url = self.base_url + self.info_uri + "/" + self.tag_id
            r = requests.delete(request_url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def _put_request(self):
        try:
            request_url = self.base_url + self.info_uri + "/" + self.tag_id
            r = requests.put(url=request_url, data=json.dumps(self.tag_name), headers=self.headers)
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def _get_request(self):
        try:
            request_url = self.base_url + self.info_uri + "/" + self.tag_id if self.tag_id else \
                self.base_url + self.info_uri
            r = requests.get(request_url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def _post_request(self):
        try:
            request_url = self.base_url + self.info_uri
            r = requests.post(url=request_url, data=json.dumps({"name": self.tag_name}), headers=self.headers)
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def set_request(self):
        if self.tag_name:
            if self.tag_id:
                response = self._put_request()
            else:
                response = self._post_request()
        else:
            if self.tag_id:
                if self.delete_tag:
                    response = self._delete_request()
                else:
                    response = self._get_request()
            else:
                response = self._get_request()
        self.response = response

    def get_response(self):
        return self.response


class Tags(object):
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
        print "Requesting all", self.__class__.__name__, "type tags"
        req = TagsConn(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri)
        req.set_request()
        response = req.get_response()
        self.response = response

    def get_by_id(self, base_url, info_uri, tag_id):
        print "Requesting", self.__class__.__name__, "having ID", tag_id
        req = TagsConn(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                       tag_id=tag_id)
        req.set_request()
        response = req.get_response()
        self.response = response

    def add(self, base_url, info_uri, name):
        req = TagsConn(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                       tag_name=name)
        req.set_request()
        response = req.get_response()
        self.response = response

    def modify(self, base_url, info_uri, tag_id, new_name):
        req = TagsConn(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                       tag_id=tag_id, tag_name=new_name)
        req.set_request()
        response = req.get_response()
        self.response = response

    def delete(self, base_url, info_uri, tag_id):
        req = TagsConn(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                       tag_id=tag_id, delete_tag=True)
        req.set_request()
        response = req.get_response()
        self.response = response

    def get_response(self):
        return self.response
