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
class test_MainClient_poller(helpers):
  def test_notAbleToStartPollerTwice(self):
    self.ethosClient.startChangeNotificationPollerThread(
      loginSession=None,
      frequency=60, #number of seconds between fetches
      pageSize=25, #number of change notifications to get per requests
      maxRequests=4 #maximum number of rquests to use in each fecth
    )

    with self.assertRaises(EllucianEthosPythonClient.CanNotStartChangeNotificationPollerTwiceException) as context:
      self.ethosClient.startChangeNotificationPollerThread(
        loginSession=None,
        frequency=60, #number of seconds between fetches
        pageSize=25, #number of change notifications to get per requests
        maxRequests=4 #maximum number of rquests to use in each fecth
      )

    self.ethosClient.close()


  def test_startThenStopPoller(self):
    pollerQueue = queue.Queue()

    self.ethosClient.startChangeNotificationPollerThread(
      loginSession=None,
      frequency=60, #number of seconds between fetches
      pageSize=25, #number of change notifications to get per requests
      maxRequests=4 #maximum number of rquests to use in each fecth
    )

    self.ethosClient.close()

