import EllucianEthosPythonClient
import unittest

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
