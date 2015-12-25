import urllib2
import json
import sys


class HMHResponse(object):
    response = None

    def __init__(self):
        pass

    def set_response(self, request):
        try:
            response = urllib2.urlopen(request)
            response_header = response.info().dict
            response_body = response.read()
            response_body = json.loads(response_body)
            self.response = {"header": response_header, "body": response_body}
        except urllib2.HTTPError, e:
            if e.code >= 500:
                print "Some issue with the server. Please try once again."
                print "or try renewing the access token."
                sys.exit(-1)
            elif e.code == 401:
                print "Invalid credentials."
                print "See if the access token is correct or renew it."
                sys.exit(-1)
            elif e.code == 404:
                print "The requested URL seems to be unavailable."
                sys.exit(-1)
            elif e.code == 403:
                print "This role probably does have access the requested URL."
                sys.exit(-1)
            else:
                print "HTTPError with code", e.code
                sys.exit(-1)
        except urllib2.URLError, e:
            print "Please see if you have the correct URL", e.errno
            sys.exit(-1)
        except Exception:
            import traceback
            print "Generic Exception", traceback.format_exc()
            sys.exit(-1)

    def get_response(self):
        return self.response


class HMHRequest(object):
    request = None
    base_url = None
    info_uri = None
    role_id = None

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
        if self.role_id:
            req = urllib2.Request(self.base_url + self.info_uri + "/" + self.role_id)
        else:
            req = urllib2.Request(self.base_url + self.info_uri)
        req.add_header("Vnd-HMH-Api-Key", self.api_key)
        req.add_header("Authorization", self.access_token)
        req.add_header("Accept", "application/json")
        req.add_header("Content-Type", "application/json")
        self.request = req

    def get_request(self):
        return self.request


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
        req = HMHRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri)
        req.set_request()
        request = req.get_request()

        resp = HMHResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def get_by_id(self, base_url, info_uri, role_id):
        print "Requesting", self.__class__.__name__, "role having refID", role_id
        req = HMHRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                         role_id=role_id)
        req.set_request()
        request = req.get_request()

        resp = HMHResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def get_response(self):
        return self.response
