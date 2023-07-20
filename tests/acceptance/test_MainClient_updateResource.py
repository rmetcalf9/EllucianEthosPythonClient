# Tests of updating a resource
import TestHelperSuperClass
import EllucianEthosPythonClient
import base64
import json
import TestingHelper

class helpers(TestHelperSuperClass.testClassWithHelpers):
  def saveResourse(
    self,
    resourceWrapperObject,
    mockResponse,
    mockResponseHeaders,
    mockResponseStatusCode
  ):
    self.ethosClient.mock.registerNextResponse(
      reqFnName="put",
      url="/api/" + resourceWrapperObject.resourceName + "/" + resourceWrapperObject.resourceID,
      data=json.dumps(resourceWrapperObject._getDictForPut()),
      status_code=mockResponseStatusCode,
      contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
      contentHeaders=mockResponseHeaders,
      ignoreData=False
    )

    resourceWrapperObject.save(loginSession=None)

class test_MainClient_updateResource(helpers):
  def test_updatePersons(self):
    personVersionInResponse = "12"
    personGUID = "testGUID"
    mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionInResponse)

    person = self.getResourse(
      guid=personGUID,
      mockResponse=mockResponse,
      mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=mockResponseStatusCode
    )
    person.dict["names"][0]["lastName"] = "ChangedLastName"

    mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionInResponse)
    mockResponse["names"][0]["lastName"] = person.dict["names"][0]["lastName"]
    self.saveResourse(
      resourceWrapperObject=person,
      mockResponse=mockResponse,
      mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=mockResponseStatusCode
    )

    #Make sure object has updated value
    self.assertEqual(person.dict["names"][0]["lastName"], "ChangedLastName")


