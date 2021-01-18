# Tests on main client object
import TestHelperSuperClass
import EllucianEthosPythonClient
import base64
import json
import TestingHelper
import queue

class helpers(TestHelperSuperClass.testClassWithHelpers):
  pass

@TestHelperSuperClass.wipd
class test_MainClient_resourceIterator(helpers):
  def test_singlePage(self):
    personGUID="personGUID"


    singlePersonResponseDict, _, _ = TestingHelper.getPersonMockResult(personGUID=personGUID, version="6")
    data=None
    mockResponse=[singlePersonResponseDict, singlePersonResponseDict, singlePersonResponseDict, singlePersonResponseDict, singlePersonResponseDict]

    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/api/persons?limit=9&offset=5",
      data=data,
      status_code=200,
      contentBytes=base64.b64encode(json.dumps([]).encode()),
      contentHeaders={
        "x-hedtech-media-type": "application/vnd.hedtech.integration.v6+json"
      },
      ignoreData=False
    )
    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/api/persons?limit=9&offset=0",
      data=data,
      status_code=200,
      contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
      contentHeaders={
        "x-hedtech-media-type": "application/vnd.hedtech.integration.v6+json"
      },
      ignoreData=False
    )

    personIterator = self.ethosClient.getResourceIterator(
      loginSession=None,
      resourceName="persons",
      version=None,
      pageSize=9
    )
    cur = 0
    for curPerson in personIterator:
      cur += 1

    self.assertEqual(cur,5)

  # Test commented out as it recreates an issue that needs to be confirmed
  # def test_responseMissingVersion(self):
  #   personGUID="personGUID"
  #
  #   singlePersonResponseDict, _, _ = TestingHelper.getPersonMockResult(personGUID=personGUID, version="6")
  #   data=None
  #   mockResponse=[singlePersonResponseDict, singlePersonResponseDict, singlePersonResponseDict, singlePersonResponseDict, singlePersonResponseDict]
  #
  #   self.ethosClient.mock.registerNextResponse(
  #     reqFnName="get",
  #     url="/api/persons?limit=9&offset=5",
  #     data=data,
  #     status_code=200,
  #     contentBytes=base64.b64encode(json.dumps([]).encode()),
  #     contentHeaders=None,
  #     # contentHeaders={
  #     #   "x-hedtech-media-type": "application/vnd.hedtech.integration.v6+json"
  #     # },
  #     ignoreData=False
  #   )
  #   self.ethosClient.mock.registerNextResponse(
  #     reqFnName="get",
  #     url="/api/persons?limit=9&offset=0",
  #     data=data,
  #     status_code=200,
  #     contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
  #     contentHeaders=None,
  #     # contentHeaders={
  #     #   "x-hedtech-media-type": "application/vnd.hedtech.integration.v6+json"
  #     # },
  #     ignoreData=False
  #   )
  #
  #   personIterator = self.ethosClient.getResourceIterator(
  #     loginSession=None,
  #     resourceName="persons",
  #     version=None,
  #     pageSize=9
  #   )
  #   cur = 0
  #   for curPerson in personIterator:
  #     cur += 1
  #
  #   self.assertEqual(cur,5)
