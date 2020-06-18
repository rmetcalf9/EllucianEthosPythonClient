# Tests on main client object
import TestHelperSuperClass
import EllucianEthosPythonClient

class helpers(TestHelperSuperClass.testClassWithHelpers):
  pass

@TestHelperSuperClass.wipd
class test_MainClient(helpers):
  def test_basicGetPerson(self):
    loginSession = None

    person = self.ethosClient.getResource(
      loginSession=loginSession,
      resourceName="persons",
      resourceID="ddd"
    )