# Tests on main client object
import TestHelperSuperClass
import EllucianEthosPythonClient
import base64
import json
import TestingHelper
import queue

class helpers(TestHelperSuperClass.testClassWithHelpers):
  pass

class test_MainClient_poller(helpers):
  def test_notAbleToStartPollerTwiceWithoutClose(self):
    pollerQueue = queue.Queue()

    mockResponse={}
    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/consume?limit=20",
      data=None,
      status_code=200,
      contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
      contentHeaders={ "x-remaining": "0"},
      ignoreData=True
    )

    self.ethosClient.startChangeNotificationPollerThread(
      loginSession=None,
      frequency=60, #number of seconds between fetches
      pageLimit=20, #number of change notifications to get per requests
      maxRequests=4, #maximum number of rquests to use in each fecth
      pollerQueue=pollerQueue
    )

    with self.assertRaises(EllucianEthosPythonClient.CanNotStartChangeNotificationPollerTwiceException) as context:
      self.ethosClient.startChangeNotificationPollerThread(
        loginSession=None,
        frequency=60, #number of seconds between fetches
        pageLimit=20, #number of change notifications to get per requests
        maxRequests=4, #maximum number of rquests to use in each fecth
        pollerQueue=pollerQueue
      )

    self.ethosClient.close()


  def test_startThenStopPoller(self):
    pollerQueue = queue.Queue()

    mockResponse={}
    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/consume?limit=20",
      data=None,
      status_code=200,
      contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
      contentHeaders={ "x-remaining": "0"},
      ignoreData=True
    )
    self.ethosClient.startChangeNotificationPollerThread(
      loginSession=None,
      frequency=60, #number of seconds between fetches
      pageLimit=20, #number of change notifications to get per requests
      maxRequests=4, #maximum number of rquests to use in each fecth
      pollerQueue=pollerQueue
    )

    self.ethosClient.close()

  def test_startThenStopPollerFunctionMode(self):

    def processSingleMessage(apiClient, messageid, changeNotification):
      # in a real example this part would write to file or update a db
      print("received ", changeNotification.operation, changeNotification.resourceName, changeNotification.resourceID)
      return True

    mockResponse={}
    self.ethosClient.mock.registerNextResponse(
      reqFnName="get",
      url="/consume?limit=20&lastProcessedID=123",
      data=None,
      status_code=200,
      contentBytes=base64.b64encode(json.dumps(mockResponse).encode()),
      contentHeaders={ "x-remaining": "0"},
      ignoreData=True
    )
    self.ethosClient.startChangeNotificationPollerThreadInFunctionMode(
      loginSession=None,
      frequency=60, #number of seconds between fetches
      pageLimit=20, #number of change notifications to get per requests
      maxRequests=4, #maximum number of rquests to use in each fecth
      lastProcessedID="123",
      messageProcessingFunction=processSingleMessage
    )

    self.ethosClient.close()

