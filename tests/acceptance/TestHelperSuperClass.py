import EllucianEthosPythonClient
import unittest
import base64
import json

from nose.plugins.attrib import attr
def wipd(f):
    return attr('wip')(f)

ethosBaseURL="MOCK"

class testClassWithHelpers(unittest.TestCase):
  ethosClient = None

  def setUp(self):
    self.ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)

  def tearDown(self):
    self.ethosClient.testComplete()
    self.ethosClient = None

  def getResourse(
      self,
      guid,
      mockResponse,
      mockResponseHeaders,
      mockResponseStatusCode,
      type="persons",
      version=None
  ):
    loginSession = None
    data=None
    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/api/" + type + "/" + guid,
      data=data,
      status_code=mockResponseStatusCode,
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
    if resp is None:
      return resp
    self.assertEqual(resp.resourceName, type)
    self.assertEqual(resp.resourceID, guid)
    return resp