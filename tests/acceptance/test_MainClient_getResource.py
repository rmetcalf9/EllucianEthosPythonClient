# Tests on main client object
import TestHelperSuperClass
import EllucianEthosPythonClient
import base64
import json
import TestingHelper

class helpers(TestHelperSuperClass.testClassWithHelpers):
  pass

@TestHelperSuperClass.wipd
class test_MainClient_getResource(helpers):
  def test_getPersonNoVersionSpecfied(self):
    personVersionInResponse = "12"
    personGUID = "testGUID"
    mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionInResponse)

    person = self.getResourse(
      guid=personGUID,
      mockResponse=mockResponse,
      mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=mockResponseStatusCode
    )
    self.assertEqual(type(person).__name__, "PersonsV" + str(personVersionInResponse))
    self.assertEqual(person.version, personVersionInResponse)

  def test_getPersonVersionSpecfiedReturnsCorrectWrapperObject(self):
    for personVersionToTest in ["6", "8", "12", "12.1.0"]:
      personGUID = "testGUID"
      mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionToTest)
      person = self.getResourse(
        guid=personGUID,
        mockResponse=mockResponse,
        mockResponseHeaders=mockResponseHeaders,
        version=personVersionToTest,
      mockResponseStatusCode=mockResponseStatusCode
      )
      if personVersionToTest == "12.1.0":
        self.assertEqual(type(person).__name__, "PersonsV12")
      else:
        self.assertEqual(type(person).__name__, "PersonsV" + personVersionToTest)

      self.assertEqual(person.version, personVersionToTest)

  def test_whenUnknownPersonVersionIsReturnedGenericResourceWrapperIsUsed(self):
      personGUID = "testGUID"
      mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonMockResult(personGUID=personGUID, version="99999")
      person = self.getResourse(
        guid=personGUID,
        mockResponse=mockResponse,
        mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=mockResponseStatusCode
      )
      self.assertEqual(type(person).__name__, "BaseResourceWrapper")
      self.assertEqual(person.version, "99999")

  def test_requestingUnknownResourceNAmeReturnsGenericResourceWrapper(self):
      guid = "testGUID"
      mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getMimimumResourceMockResult(guid=guid, version="99999")
      resourceWrapper = self.getResourse(
        guid=guid,
        mockResponse=mockResponse,
        mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=mockResponseStatusCode
      )
      self.assertEqual(type(resourceWrapper).__name__, "BaseResourceWrapper")
      self.assertEqual(resourceWrapper.version, "99999")

  def test_getNonExistantPerson(self):
    personVersionInResponse = "12"
    personGUID = "testGUID"
    mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonNotFoundMockResult(personGUID=personGUID, version=personVersionInResponse)

    person = self.getResourse(
      guid=personGUID,
      mockResponse=mockResponse,
      mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=mockResponseStatusCode
    )
    self.assertEqual(person, None)

  def test_refreshPersonNoVersionSpecfied(self):
    personVersionInResponse = "12"
    personGUID = "testGUID"
    mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionInResponse)

    person = self.getResourse(
      guid=personGUID,
      mockResponse=mockResponse,
      mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=mockResponseStatusCode
    )
    self.assertEqual(type(person).__name__, "PersonsV" + str(personVersionInResponse))
    self.assertEqual(person.version, personVersionInResponse)
    self.assertEqual(person.dict["names"][0]["firstName"],"Joe")

    mockResponse2, mockResponseHeaders2, mockResponseStatusCode2 = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionInResponse, firstName="Joe Number 2")
    data=None
    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/api/" + "persons" + "/" + personGUID,
      data=data,
      status_code=mockResponseStatusCode2,
      contentBytes=base64.b64encode(json.dumps(mockResponse2).encode()),
      contentHeaders=mockResponseHeaders2,
      ignoreData=False
    )
    person.refresh(loginSession=None)

    self.assertEqual(type(person).__name__, "PersonsV" + str(personVersionInResponse))
    self.assertEqual(person.version, personVersionInResponse)
    self.assertEqual(person.dict["names"][0]["firstName"],"Joe Number 2")

  def test_requestingUnknownResourceNameWithGUIDratherThanID_ReturnsGenericResourceWrapper(self):
      guid = "testGUID"
      mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getMimimumResourceMockResult(guid=guid, version="99999", useGUIDasIDKey=True)
      resourceWrapper = self.getResourse(
        guid=guid,
        mockResponse=mockResponse,
        mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=mockResponseStatusCode
      )
      self.assertEqual(type(resourceWrapper).__name__, "BaseResourceWrapper")
      self.assertEqual(resourceWrapper.version, "99999")

