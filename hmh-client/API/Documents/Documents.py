import urllib2
import json
from urllib import quote_plus, urlencode
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import sys


class DocumentsResponse(object):
    response = None

    def __init__(self, file_upload=False):
        self.file_upload = file_upload

    def set_response(self, request, file_obj=None):
        try:
            response = urllib2.urlopen(request)
            if self.file_upload and file_obj:
                file_obj.close()
            response_header = response.info().dict
            response_body = response.read()
            response_body = json.loads(response_body)
            self.response = {"header": response_header, "body": response_body}
        except urllib2.HTTPError, e:
            if e.code >= 500:
                print "Some issue with the server. Please try once again."
                print "or try renewing the access token."
                print e.code
            elif e.code == 401:
                print "Invalid credentials."
                print "See if the access token is correct or renew it."
            elif e.code == 404:
                print "The requested URL seems to be unavailable."
            elif e.code == 403:
                print "This role probably does have access the requested URL."
            else:
                print "HTTPError with code", e.code
        except urllib2.URLError, e:
            print "Please see if you have the correct URL", e.errno
        except Exception:
            import traceback
            print "Generic Exception", traceback.format_exc()

    def get_response(self):
        return self.response


class DocumentModel(object):
    def __init__(self, title=None, url=None, tags=None, note_html=None):
        self.title = title
        self.url = url
        self.tags = tags
        self.note_html = note_html

    def to_json(self):
        return {
            "title": self.title,
            "url": self.url,
            "tags": self.tags,
            "note_html": self.note_html
        }


class DocumentsRequest(object):
    request = None
    base_url = None
    info_uri = None
    document_id = None
    doc_model = None
    file_path = None
    delete_document = None
    filter_uuids = None
    filter_tags = None
    file_obj = None

    def __init__(self, access_token, api_key, base_url, info_uri, document_id=None, doc_model=None, file_path=None,
                 delete_document=False, filter_uuids=None, filter_tags=None):
        self.base_url = base_url
        self.info_uri = info_uri
        self._set_access_token(access_token)
        self._set_api_key(api_key)
        self.document_id = document_id
        self.doc_model = doc_model
        self.file_path = file_path
        self.delete_document = delete_document
        self.filter_uuids = filter_uuids
        self.filter_tags = filter_tags

    def _set_access_token(self, access_token):
        assert isinstance(access_token, (str, unicode)), access_token
        self.access_token = access_token

    def _set_api_key(self, api_key):
        assert isinstance(api_key, (str, unicode)), api_key
        self.api_key = api_key

    def _delete_request(self):
        req = urllib2.Request(self.base_url + self.info_uri + "/" + self.document_id)
        req.get_method = lambda: "DELETE"
        return req

    def _put_request(self):
        req = urllib2.Request(self.base_url + self.info_uri + "/" + self.document_id)
        req.get_method = lambda: "PUT"
        req.add_data(json.dumps({"document": self.doc_model.to_json()}))
        return req

    def _add_document(self):
        try:
            print "Beginning upload of document"
            register_openers()
            f = open(self.file_path, "rb")
            datagen, headers = multipart_encode([("file", f), ("document", json.dumps(self.doc_model.to_json()))])
            req = urllib2.Request(self.base_url + self.info_uri, data=datagen, headers=headers)
            print "Upload done"
            return req, f
        except Exception as e:
            print e.message
            sys.exit(-1)

    def _filtered_request(self):
        values = {}
        if self.filter_uuids:
            values["include"] = quote_plus(self.filter_uuids)
        if self.filter_tags:
            values["filter_tags"] = quote_plus(self.filter_tags)
        data = urlencode(values)
        req = urllib2.Request(self.base_url + self.info_uri, data=data)
        return req

    def set_request(self):
        if self.document_id:
            if self.doc_model:
                req = self._put_request()
            else:
                if self.delete_document:
                    req = self._delete_request()
                else:
                    req = urllib2.Request(self.base_url + self.info_uri + "/" + self.document_id)
        else:
            if self.doc_model and self.file_path:
                req, f = self._add_document()
                self.file_obj = f
            else:
                if self.filter_uuids or self.filter_tags:
                    req = self._filtered_request()
                else:
                    req = urllib2.Request(self.base_url + self.info_uri)
        req.add_header("Vnd-HMH-Api-Key", self.api_key)
        req.add_header("Authorization", self.access_token)
        req.add_header("Accept", "application/json")
        req.add_header("Content-Type", "application/json")
        self.request = req
        assert self.request

    def get_request(self):
        return self.request

    def get_upload_file_object(self):
        return self.file_obj


class Documents(object):
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
        print "Requesting all", self.__class__.__name__, "type objects"
        req = DocumentsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                               info_uri=info_uri)
        req.set_request()
        request = req.get_request()

        resp = DocumentsResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def get_by_id(self, base_url, info_uri, document_id):
        print "Requesting", self.__class__.__name__, "having ID", document_id
        req = DocumentsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                               info_uri=info_uri, document_id=document_id)
        req.set_request()
        request = req.get_request()

        resp = DocumentsResponse()
        resp.set_response(request=request)
        response = resp.get_response()
        self.response = response

    def add(self, base_url, info_uri, file_path, doc_model):
        print "Adding the file at ", file_path
        req = DocumentsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                               info_uri=info_uri, file_path=file_path, doc_model=doc_model)
        req.set_request()
        request = req.get_request()
        upload_file = req.get_upload_file_object()

        resp = DocumentsResponse(file_upload=True)
        resp.set_response(request=request, file_obj=upload_file)
        response = resp.get_response()
        self.response = response

    # def modify(self, base_url, info_uri, tag_id, new_name):
    #     req = TagsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
    #                       tag_id=tag_id, tag_name=new_name)
    #     req.set_request()
    #     request = req.get_request()
    #
    #     resp = TagsResponse()
    #     resp.set_response(request=request)
    #     response = resp.get_response()
    #     self.response = response

    # def delete_tag(self, base_url, info_uri, tag_id):
    #     req = TagsRequest(access_token=self.access_token, api_key=self.api_key, base_url=base_url, info_uri=info_uri,
    #                       tag_id=tag_id, delete_tag=True)
    #     req.set_request()
    #     request = req.get_request()
    #
    #     resp = TagsResponse()
    #     resp.set_response(request=request)
    #     response = resp.get_response()
    #     self.response = response

    def get_response(self):
        return self.response
