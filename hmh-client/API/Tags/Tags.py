import urllib2
import json
import sys


class TagsResponse(object):
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

    def get_response(self):
        return self.response


class TagsRequest(object):
    request = None
    base_url = None
    info_uri = None
    role_id = None

    def __init__(self, access_token, api_key, base_url, info_uri, tag_id=None, tag_name=None, delete_tag=False):
        self.base_url = base_url
        self.info_uri = info_uri
        self._set_access_token(access_token)
        self._set_api_key(api_key)
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.delete_tag = delete_tag

    def _set_access_token(self, access_token):
        assert isinstance(access_token, (str, unicode)), access_token
        self.access_token = access_token

    def _set_api_key(self, api_key):
        assert isinstance(api_key, (str, unicode)), api_key
        self.api_key = api_key

    def _delete_request(self):
        assert self.tag_id
        req = urllib2.Request(self.base_url + self.info_uri + "/" + self.tag_id)
        req.get_method = lambda: "DELETE"
        return req

    def _put_request(self):
        request_url = self.base_url + self.info_uri + "/" + self.tag_id if (self.tag_id and self.tag_name) \
            else self.base_url + self.info_uri
        req = urllib2.Request(request_url)
        req.add_data(json.dumps({"name": self.tag_name}))
        return req

    def set_request(self):
        if self.tag_id:
            if self.tag_name:
                req = self._put_request()
                req.get_method = lambda: "PUT"
            elif self.delete_tag:
                req = self._delete_request()
            else:
                req = urllib2.Request(self.base_url + self.info_uri + "/" + self.tag_id)
        elif self.tag_name:
            req = self._put_request()
        else:
            req = urllib2.Request(self.base_url + self.info_uri)
        req.add_header("Vnd-HMH-Api-Key", self.api_key)
        req.add_header("Authorization", self.access_token)
        req.add_header("Accept", "application/json")
        req.add_header("Content-Type", "application/json")
        self.request = req

    def get_request(self):
        return self.request


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
        req = TagsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri)
        req.set_request()
        request = req.get_request()

        resp = TagsResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def get_by_id(self, base_url, info_uri, tag_id):
        print "Requesting", self.__class__.__name__, "having ID", tag_id
        req = TagsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                          tag_id=tag_id)
        req.set_request()
        request = req.get_request()

        resp = TagsResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def add(self, base_url, info_uri, name):
        req = TagsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                          tag_name=name)
        req.set_request()
        request = req.get_request()

        resp = TagsResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def modify(self, base_url, info_uri, tag_id, new_name):
        req = TagsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                          tag_id=tag_id, tag_name=new_name)
        req.set_request()
        request = req.get_request()

        resp = TagsResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def delete_tag(self, base_url, info_uri, tag_id):
        req = TagsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
                          tag_id=tag_id, delete_tag=True)
        req.set_request()
        request = req.get_request()

        resp = TagsResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def get_response(self):
        return self.response
