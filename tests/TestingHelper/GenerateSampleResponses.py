# This file contains generators for sample responses

def getMimimumResourceMockResult(
  guid,
  version,
  useGUIDasIDKey=False
):
  responseHeaders = { "x-hedtech-media-type": "application/vnd.hedtech.integration.v" + version + "+json"}
  guidKey = "id"
  if useGUIDasIDKey:
    guidKey = "guid"

  response = {
    guidKey: guid,
  }
  return response, responseHeaders, 200

def getPersonMockResult(
  personGUID,
  version,
  firstName="Joe"
):
  responseHeaders = { "x-hedtech-media-type": "application/vnd.hedtech.integration.v" + version + "+json"}
  response = {
    "addresses": [],
    "credentials": [],
    "dateOfBirth": "1996-04-11",
    "emails": [],
    "gender": "male",
    "id": personGUID,
    "names": [
      {"firstName": firstName, "fullName": "Joe Blogs", "lastName": "Blogs", "preference": "preferred", "title": "Mr",
       "type": {"category": "personal"}}],
    "privacyStatus": {"privacyCategory": "unrestricted"},
    "roles": [{"role": "student", "startOn": "2020-01-01T00:00:00+00:00"}]
  }
  return response, responseHeaders, 200


def getPersonNotFoundMockResult(
  personGUID,
  version
):
  responseHeaders = { "x-hedtech-media-type": "application/vnd.hedtech.integration.errors.v2+json"}
  response = {"errors":[{"code":"Global.SchemaValidation.Error","description":"Errors parsing input JSON.","message":"Person not found"}]}
  return response, responseHeaders, 404

def getPersonHoldMockResult(
    personholdGUID,
    personGUID,
    personHoldCategoryGUID,
    version
):
  responseHeaders = { "x-hedtech-media-type": "application/vnd.hedtech.integration.v" + version + "+json"}
  response = {
    "endOn":"2099-12-31T00:00:00Z",
    "id": personholdGUID,
    "person":{"id": personGUID},
    "startOn":"2020-01-17T00:00:00Z",
    "type":{
      "category":"academic",
      "detail":{"id": personHoldCategoryGUID}
    }
  }

  return response, responseHeaders, 200
