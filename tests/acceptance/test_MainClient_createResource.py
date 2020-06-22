# Tests on main client object
import TestHelperSuperClass
import EllucianEthosPythonClient
import base64
import json
import TestingHelper

class helpers(TestHelperSuperClass.testClassWithHelpers):
  def createResource(
      self,
      resourceName,
      resourceDict,
      mockResponse,
      mockResponseHeaders,
      mockResponseStatusCode,
      type,
      version=None
  ):
    self.ethosClient.mock.registerNextResponse(
      reqFnName="post",
      url="/api/" + resourceName,
      data=json.dumps(resourceDict),
      status_code=mockResponseStatusCode,
      contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
      contentHeaders=mockResponseHeaders,
      ignoreData=False
    )

    resp = self.ethosClient.createResource(
      loginSession=None,
      resourceName=type,
      resourceDict=resourceDict,
      version=version
    )
    self.assertEqual(resp.resourceName, type)
    self.assertFalse(resp.resourceID is None)
    return resp

@TestHelperSuperClass.wipd
class test_MainClient_createResource(helpers):
  def test_createPersonHold(self):
    createdPersonHoldGUID = "testPersonHoldGUID"
    personGUID = "testGUID"
    personHoldCategoryGUID = "personHoldCategoryGUID"
    personHold = {
      'endOn': '2099-12-31T00:00:00Z',
      'person': {'id': personGUID},
      'startOn': '2020-01-17T00:00:00Z',
      'type': {
        'category': 'academic',
        'detail': {
          'id': personHoldCategoryGUID
        }
      }
    }
    version="6"

    mockResponse, mockResponseHeaders, mockResponseStatusCode = TestingHelper.getPersonHoldMockResult(
      personholdGUID=createdPersonHoldGUID,
      personGUID=personGUID,
      personHoldCategoryGUID=personHoldCategoryGUID,
      version=version
    )

    createdPersonHold = self.createResource(
      resourceName="person-holds",
      resourceDict=personHold,
      mockResponse=mockResponse,
      mockResponseHeaders=mockResponseHeaders,
      mockResponseStatusCode=201,
      type="person-holds",
      version=version
    )

    self.assertEqual(createdPersonHold.version, version)

