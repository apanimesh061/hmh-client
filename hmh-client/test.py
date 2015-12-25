from API.Identity.V1.Roles import *
from API.Assignments.Assignments import *
from API.Tags.Tags import *
from API.Documents.Documents import *
from ApplicationToken import *
from Constants import *
from pprint import pprint

if __name__ == "__main2__":
    client = HmhClient(request_url=BASE_URL + ACCESS_TOKEN_URL,
                       hmh_api_key=HMH_CLIENT_API_KEY,
                       client_id=CLIENT_ID,
                       grant_type="password",
                       username="sauron",
                       password="password")
    response_body = client.get_response()
    pprint(response_body)
    HmhClient.save_as(response_body, "sauron_credentials.pkl")

if __name__ == "__main22__":
    credentials = cPickle.load(open("sauron_credentials.pkl", "rb"))
    pprint(credentials)
    client = HmhClient(request_url=BASE_URL + ACCESS_TOKEN_URL,
                       hmh_api_key=HMH_CLIENT_API_KEY,
                       client_id=CLIENT_ID,
                       grant_type="refresh_token",
                       username="sauron",
                       password="password",
                       refresh_token=credentials["refresh_token"])
    response_body = client.get_response()
    pprint(response_body)

if __name__ == "__main2__":
    credentials = cPickle.load(open("credentials.pkl", "rb"))
    s = School()
    s.set_access_token(credentials["access_token"])
    s.set_api_key(HMH_CLIENT_API_KEY)
    s.get_all(BASE_URL, V1_SCHOOLS_INFO)
    pprint(s.get_response())

if __name__ == "__main1__":
    credentials = cPickle.load(open("sauron_credentials.pkl", "rb"))
    s = Assignments()
    s.set_access_token(credentials["access_token"])
    s.set_api_key(HMH_CLIENT_API_KEY)
    s.get_all(BASE_URL, V1_ASSIGNMENTS_INFO_URI)
    pprint(s.get_response())
    exit()
    # s.get_by_id(BASE_URL, V1_ASSIGNMENTS_INFO_URI, role_id="f335f82a-1891-4e9c-863a-7113981b032d")
    s.get_by_id(BASE_URL, V1_ASSIGNMENTS_INFO_URI_INDIVIDUAL_SUBMISSIONS,
                role_id="f335f82a-1891-4e9c-863a-7113981b032d", check_submissions=True)
    pprint(s.get_response()["body"])

    # s1 = Student()
    # s1.set_access_token(credentials["access_token"])
    # s1.set_api_key(HMH_CLIENT_API_KEY)
    # s1.get_by_id(BASE_URL, V1_STUDENT_INFO, role_id="0c127e7b-3b97-4d9d-a802-5acbca54097a")
    # pprint(s1.get_response().get("body"))

if __name__ == "__main11__":
    credentials = cPickle.load(open("sauron_credentials.pkl", "rb"))
    t = Tags()
    t.set_access_token(credentials["access_token"])
    t.set_api_key(HMH_CLIENT_API_KEY)
    # t.get_all(BASE_URL, V1_TAGS_INFO_URI)
    t.get_by_id(BASE_URL, V1_TAGS_INFO_URI, tag_id="897")
    # t.add(BASE_URL, V1_TAGS_INFO_URI, name="python")
    # t.delete_tag(BASE_URL, V1_TAGS_INFO_URI, tag_id="896")
    # t.modify(BASE_URL, V1_TAGS_INFO_URI, tag_id="897", new_name="boa")
    pprint(t.get_response()["body"])

if __name__ == "__main__":
    credentials = cPickle.load(open("sauron_credentials.pkl", "rb"))
    d = Documents()
    d.set_access_token(credentials["access_token"])
    d.set_api_key(HMH_CLIENT_API_KEY)
    # d.get_all(BASE_URL, V1_DOCUMENTS_INFO_URI)
    # d.get_by_id(BASE_URL, V1_DOCUMENTS_INFO_URI, document_id="1ccf67fe-0824-489f-b65c-0632dc6edce5")
    new_doc_model = DocumentModel(title="New Document", url="", tags=["new", "docx", "hmh"], note_html="")
    d.add(BASE_URL, V1_DOCUMENTS_INFO_URI, file_path="F:\\PyCharmProjects\\hmh-client\\hmh-client\\new_doc.pdf",
          doc_model=new_doc_model)
    res = d.get_response()["body"]
    pprint(res)
