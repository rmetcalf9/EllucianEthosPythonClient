# Tests on main client object
import TestHelperSuperClass
import EllucianEthosPythonClient
import base64
import json
import TestingHelper

class helpers(TestHelperSuperClass.testClassWithHelpers):
  def getResourse(
      self,
      guid,
      mockResponse,
      mockResponseHeaders,
      type="persons",
      version=None
  ):
    loginSession = None
    data=None
    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/api/" + type + "/" + guid,
      data=data,
      status_code=200,
      contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
      contentHeaders=mockResponseHeaders,
      ignoreData=False
    )

    resp = self.ethosClient.getResource(
      loginSession=loginSession,
      resourceName=type,
      resourceID=guid,
      version=version
    )
    self.assertEqual(resp.resourceName, type)
    self.assertEqual(resp.resourceID, guid)
    return resp

@TestHelperSuperClass.wipd
class test_MainClient(helpers):
  def test_getPersonNoVersionSpecfied(self):
    personVersionInResponse = "12"
    personGUID = "testGUID"
    mockResponse, mockResponseHeaders = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionInResponse)

    person = self.getResourse(
      guid=personGUID,
      mockResponse=mockResponse,
      mockResponseHeaders=mockResponseHeaders
    )
    self.assertEqual(type(person).__name__, "PersonsV" + str(personVersionInResponse))
    self.assertEqual(person.version, personVersionInResponse)

  def test_getPersonVersionSpecfiedReturnsCorrectWrapperObject(self):
    for personVersionToTest in ["6", "8", "12", "12.1.0"]:
      personGUID = "testGUID"
      mockResponse, mockResponseHeaders = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionToTest)
      person = self.getResourse(
        guid=personGUID,
        mockResponse=mockResponse,
        mockResponseHeaders=mockResponseHeaders,
        version=personVersionToTest
      )
      if personVersionToTest == "12.1.0":
        self.assertEqual(type(person).__name__, "PersonsV12")
      else:
        self.assertEqual(type(person).__name__, "PersonsV" + personVersionToTest)

      self.assertEqual(person.version, personVersionToTest)

  def test_whenUnknownPersonVersionIsReturnedGenericResourceWrapperIsUsed(self):
      personGUID = "testGUID"
      mockResponse, mockResponseHeaders = TestingHelper.getPersonMockResult(personGUID=personGUID, version="99999")
      person = self.getResourse(
        guid=personGUID,
        mockResponse=mockResponse,
        mockResponseHeaders=mockResponseHeaders
      )
      self.assertEqual(type(person).__name__, "BaseResourceWrapper")
      self.assertEqual(person.version, "99999")

  def test_requestingUnknownResourceNAmeReturnsGenericResourceWrapper(self):
      guid = "testGUID"
      mockResponse, mockResponseHeaders = TestingHelper.getMimimumResourceMockResult(guid=guid, version="99999")
      resourceWrapper = self.getResourse(
        guid=guid,
        mockResponse=mockResponse,
        mockResponseHeaders=mockResponseHeaders
      )
      self.assertEqual(type(resourceWrapper).__name__, "BaseResourceWrapper")
      self.assertEqual(resourceWrapper.version, "99999")
