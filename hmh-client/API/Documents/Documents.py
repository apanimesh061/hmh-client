import sys
import requests
from requests import exceptions
import json


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


class DocumentsConnection(object):
    response = None
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
        if filter_tags:
            assert isinstance(filter_tags, list), filter_tags
        if filter_uuids:
            assert isinstance(filter_uuids, list), filter_uuids
        self.filter_uuids = filter_uuids
        self.filter_tags = filter_tags
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
        pass

    def _put_request(self):
        pass

    def _filtered_request(self, request_url):
        values = {}
        if self.filter_uuids:
            values["include"] = str(self.filter_uuids)
        if self.filter_tags:
            values["filter_tags"] = str(self.filter_tags)
        r = requests.get(request_url, headers=self.headers, params=values)
        return r

    def _get_request(self):
        try:
            request_url = self.base_url + self.info_uri + "/" + self.document_id if self.document_id else \
                self.base_url + self.info_uri
            if self.filter_tags or self.filter_uuids:
                r = self._filtered_request(request_url=request_url)
            else:
                r = requests.get(request_url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def _post_request(self):
        try:
            request_url = self.base_url + self.info_uri
            with open(self.file_path, "rb") as f:
                files = {
                    "file": f
                }
                payload = {
                    "document": self.doc_model.to_json()
                }
                r = requests.post(request_url, files=files)
                r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)
        except IOError as e:
            print e
            sys.exit(-1)
        finally:
            if r.status_code == requests.codes.unauthorized:
                print "unauthorized"
            if r.status_code == requests.codes.ok:
                print "OK"

    def set_request(self):
        if self.document_id:
            if self.doc_model:
                response = self._put_request()
            else:
                if self.delete_document:
                    response = self._delete_request()
                else:
                    response = self._get_request()
        else:
            if self.doc_model and self.file_path:
                response = self._post_request()
            else:
                if self.filter_uuids or self.filter_tags:
                    response = self._get_request()
                else:
                    response = self._get_request()
        self.response = response

    def get_response(self):
        return self.response


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

    def get_all(self, base_url, info_uri, filter_tags=None, filter_uuids=None):
        print "Requesting all", self.__class__.__name__, "type objects"
        req = DocumentsConnection(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                                  info_uri=info_uri, filter_tags=filter_tags, filter_uuids=filter_uuids)
        req.set_request()
        response = req.get_response()
        self.response = response

    def get_by_id(self, base_url, info_uri, document_id):
        print "Requesting", self.__class__.__name__, "having ID", document_id
        req = DocumentsConnection(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                                  info_uri=info_uri, document_id=document_id)
        req.set_request()
        response = req.get_response()
        self.response = response

    def add(self, base_url, info_uri, file_path, doc_model):
        req = DocumentsConnection(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                                  info_uri=info_uri, file_path=file_path, doc_model=doc_model)
        req.set_request()
        response = req.get_response()
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
