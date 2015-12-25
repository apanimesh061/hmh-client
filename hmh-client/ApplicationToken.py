import urllib2
from urllib import urlencode
import json
import cPickle
import sys


class Object(object):
    def __init__(self, **response):
        for k, v in response.iteritems():
            if isinstance(v, dict):
                self.__dict__[k] = Object(**v)
            else:
                self.__dict__[k] = v


class HmhClient(object):
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
            "password": self.password
        }
        if self.grant_type == "refresh_token" and self.refresh_token:
            values["refresh_token"] = self.refresh_token

        data = urlencode(values)
        req = urllib2.Request(self.request_url, data)
        req.add_header("Vnd-HMH-Api-Key", self.hmh_api_key)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:
            response = urllib2.urlopen(req)
            response_header = response.info().dict
            response_body = response.read()

            json_acceptable_string = response_body.replace("'", "\"")
            response_body_dict = json.loads(json_acceptable_string)

            temp = response_body_dict['sub']
            response_body_dict['sub'] = dict(map(lambda a: a.split("="), temp.split(',')))
            return response_body_dict
        except urllib2.HTTPError, e:
            if e.code >= 500:
                print "Some issue with the server. Please try once again."
                print "or try renewing the access token."
            elif e.code == 401:
                print "Invalid credentials."
                print "See if the access token is correct or renew it."
            elif e.code == 404:
                print "The requested URL seems to be unavailable."
            elif e.code == 403:
                print "This role probably does have access the requested URL."
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

    @staticmethod
    def to_object(response):
        return Object(**response)

    @staticmethod
    def save_as(tokens, filename):
        return cPickle.dump(tokens, open(filename, "wb"))
