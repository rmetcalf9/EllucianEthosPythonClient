# This file contains generators for sample responses

def getMimimumResourceMockResult(
  guid,
  version
):
  responseHeaders = { "x-hedtech-media-type": "application/vnd.hedtech.integration.v" + str(version) + "+json"}
  response = {
    "id": guid,
  }
  return response, responseHeaders

def getPersonMockResult(
  personGUID,
  version
):
  responseHeaders = { "x-hedtech-media-type": "application/vnd.hedtech.integration.v" + str(version) + "+json"}
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
  return response, responseHeaders
