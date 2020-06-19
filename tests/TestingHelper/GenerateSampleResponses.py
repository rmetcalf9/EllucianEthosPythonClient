# This file contains generators for sample responses

def getMimimumResourceMockResult(
  guid,
  version
):
  responseHeaders = { "x-hedtech-media-type": "application/vnd.hedtech.integration.v" + version + "+json"}
  response = {
    "id": guid,
  }
  return response, responseHeaders, 200

def getPersonMockResult(
  personGUID,
  version
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
      {"firstName": "Joe", "fullName": "Joe Blogs", "lastName": "Blogs", "preference": "preferred", "title": "Mr",
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

