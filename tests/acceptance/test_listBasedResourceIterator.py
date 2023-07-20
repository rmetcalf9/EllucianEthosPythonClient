# Tests on main client object
import TestHelperSuperClass
import EllucianEthosPythonClient
import base64
import json
import TestingHelper
import queue

class helpers(TestHelperSuperClass.testClassWithHelpers):
  pass

class test_MainClient_listBasedResourceIterator(helpers):
  def test_emptyList(self):
    resourceIDList = []

    personIterator = self.ethosClient.getListBasedResourceIterator(
      loginSession=None,
      resourceName="persons",
      version=None,
      resourceIDList=[]
    )
    cur = 0
    for curPerson in personIterator:
      cur += 1

    self.assertEqual(cur,0)

  def test_singleItemList(self):
    personVersionInResponse = "12"
    personGUID = "testGUID"
    resourceIDList = [ personGUID ]

    personIterator = self.ethosClient.getListBasedResourceIterator(
      loginSession=None,
      resourceName="persons",
      version=None,
      resourceIDList=resourceIDList
    )
    cur = 0

    mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonMockResult(personGUID=personGUID, version=personVersionInResponse)
    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/api/persons/" + personGUID,
      data=None,
      status_code=mockResponseStatusCode,
      contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
      contentHeaders=mockResponseHeaders,
      ignoreData=False
    )

    for curPerson in personIterator:
      cur += 1
      self.assertEqual(type(curPerson).__name__, "PersonsV" + str(personVersionInResponse))
      self.assertEqual(curPerson.version, personVersionInResponse)
      self.assertEqual(curPerson.dict["names"][0]["firstName"], "Joe")


    self.assertEqual(cur,1)

