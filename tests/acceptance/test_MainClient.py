# Tests on main client object
import TestHelperSuperClass
import EllucianEthosPythonClient

class helpers(TestHelperSuperClass.testClassWithHelpers):
  pass

@TestHelperSuperClass.wipd
class test_MainClient(helpers):
  def test_basicCreation(self):
    ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=TestHelperSuperClass.ethosBaseURL)

    ethosClient.sendGetRequest(
      loginSession = None,
      url = "DD"
    )