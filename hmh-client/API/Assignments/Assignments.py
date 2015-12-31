import sys
import json

import requests
from requests import exceptions


class SourceObject(object):
    def __init__(self, ref_object=None, isbn=None, custom_lesson_id=None, value=None):
        if ref_object:
            assert isinstance(ref_object, (str, unicode)), ref_object
        if isbn:
            assert isinstance(isbn, (str, unicode)), isbn
        if custom_lesson_id:
            assert isinstance(custom_lesson_id, (str, unicode)), custom_lesson_id
        if value:
            assert isinstance(value, (str, unicode)), value
        self.ref_object = ref_object
        self.isbn = isbn
        self.custom_lesson_id = custom_lesson_id
        self.value = value

    def to_json(self):
        return {
            "refObject": self.ref_object,
            "isbn": self.isbn,
            "customLessonId": self.custom_lesson_id,
            "value": self.value
        }


class AssignmentModel(object):
    def __init__(self,
                 school_ref_id=None,
                 lea_ref_id=None,
                 section_ref_id=None,
                 students=None,
                 ref_id=None,
                 staff_ref_id=None,
                 available_date=None,
                 due_date=None,
                 name=None,
                 description=None,
                 creator_ref_id=None,
                 administrator_ref_id=None,
                 source_objects=None,
                 status=None):
        if school_ref_id:
            assert isinstance(school_ref_id, (str, unicode)), school_ref_id
        if lea_ref_id:
            assert isinstance(lea_ref_id, (str, unicode)), lea_ref_id
        if section_ref_id:
            assert isinstance(section_ref_id, (str, unicode)), section_ref_id
        if students:
            assert isinstance(students, list), students
        if ref_id:
            assert isinstance(ref_id, (str, unicode)), ref_id
        if staff_ref_id:
            assert isinstance(staff_ref_id, (str, unicode)), staff_ref_id
        if available_date:
            assert isinstance(available_date, (str, unicode)), available_date
        if due_date:
            assert isinstance(due_date, (str, unicode)), due_date
        if name:
            assert isinstance(name, (str, unicode)), name
        if description:
            assert isinstance(description, (str, unicode)), description
        if creator_ref_id:
            assert isinstance(creator_ref_id, (str, unicode)), creator_ref_id
        if administrator_ref_id:
            assert isinstance(administrator_ref_id, (str, unicode)), administrator_ref_id
        if source_objects:
            assert isinstance(source_objects, list), source_objects
        if status:
            assert isinstance(status, (str, unicode)), status
        self.school_ref_id = school_ref_id
        self.lea_ref_id = lea_ref_id
        self.section_ref_id = section_ref_id
        self.students = students
        self.ref_id = ref_id
        self.staff_ref_id = staff_ref_id
        self.available_date = available_date
        self.due_date = due_date
        self.name = name
        self.description = description
        self.creator_ref_id = creator_ref_id
        self.administrator_ref_id = administrator_ref_id
        self.source_objects = source_objects
        self.status = status

    def to_json(self):
        return {
            "schoolRefId": self.school_ref_id,
            "leaRefId": self.lea_ref_id,
            "sectionRefId": self.section_ref_id,
            "students": self.students,
            "refId": self.ref_id,
            "staffRefId": self.staff_ref_id,
            "availableDate": self.available_date,
            "dueDate": self.due_date,
            "name": self.name,
            "description": self.description,
            "creatorRefId": self.creator_ref_id,
            "administratorRefId": self.administrator_ref_id,
            "sourceObjects": self.source_objects,
            "status": self.status
        }


class AssignmentConnectionHandler(object):
    base_url = None
    info_uri = None
    role_id = None
    response = None

    def __init__(self, access_token, api_key, base_url, info_uri, assignment_id=None, assignment_model=None,
                 check_submissions=False, modify=False):
        self.base_url = base_url
        self.info_uri = info_uri
        self._set_access_token(access_token)
        self._set_api_key(api_key)
        self.assignment_id = assignment_id
        self.modify = modify
        self.check_submissions = check_submissions
        self.assignment_model = assignment_model
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

    def _patch_request(self):
        try:
            request_url = self.base_url + self.info_uri + "/" + self.assignment_id
            r = requests.patch(request_url, headers=self.headers, data=json.dumps(self.assignment_model.to_json()))
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def _get_request(self):
        try:
            if self.assignment_id:
                if self.check_submissions:
                    request_url = self.base_url + self.info_uri + "/" + self.assignment_id + "/assignmentSubmissions"
                else:
                    request_url = self.base_url + self.info_uri + "/" + self.assignment_id
            else:
                request_url = self.base_url + self.info_uri
            r = requests.get(request_url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def _post_request(self):
        try:
            request_url = self.base_url + self.info_uri
            r = requests.post(request_url, headers=self.headers, data=json.dumps(self.assignment_model.to_json()))
            r.raise_for_status()
            return r.json()
        except exceptions.RequestException as e:
            print e
            sys.exit(-1)

    def set_request(self):
        if self.assignment_id:
            if self.check_submissions:
                response = self._get_request()
            else:
                if self.modify and self.assignment_model:
                    response = self._patch_request()
                else:
                    response = self._get_request()
        else:
            if self.assignment_model:
                response = self._post_request()
            else:
                response = self._get_request()
        self.response = response

    def get_response(self):
        return self.response


class Assignments(object):
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
        req = AssignmentConnectionHandler(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                                          info_uri=info_uri)
        req.set_request()
        response = req.get_response()
        self.response = response

    def get_by_id(self, base_url, info_uri, assignment_id):
        print "Requesting", self.__class__.__name__, "having ID", assignment_id
        req = AssignmentConnectionHandler(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                                          info_uri=info_uri, assignment_id=assignment_id)
        req.set_request()
        response = req.get_response()
        self.response = response

    def get_submissions_by_id(self, base_url, info_uri, assignment_id):
        print "Requesting all submissions of", self.__class__.__name__, "having ID", assignment_id
        req = AssignmentConnectionHandler(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                                          info_uri=info_uri, assignment_id=assignment_id, check_submissions=True)
        req.set_request()
        response = req.get_response()
        self.response = response

    def add(self, base_url, info_uri, assignment_model):
        req = AssignmentConnectionHandler(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                                          info_uri=info_uri, assignment_model=assignment_model)
        req.set_request()
        response = req.get_response()
        self.response = response

    def modify(self, base_url, info_uri, assignment_id, assignment_model):
        req = AssignmentConnectionHandler(access_token=self.access_token, api_key=self.api_key, base_url=base_url,
                                          info_uri=info_uri, assignment_id=assignment_id,
                                          assignment_model=assignment_model)
        req.set_request()
        response = req.get_response()
        self.response = response

    def get_response(self):
        return self.response
