from .WorkerThread import WorkerThread
from .ChangeNotificationMessage import ChangeNotificationMessage
import json

#Ellucian documentation for this
# - https://resources.elluciancloud.com/bundle/ethos_integration_ref_apis/page/r_message_queue_api_retrieve_msgs.html

class EthosChangeNotificationPollerThreadExceptionClass(Exception):
  pass

class EthosChangeNotificationPollerThread(WorkerThread):
  clientAPIInstance = None
  loginSession = None
  pageLimit = None
  maxRequests = None
  pollerQueue = None

  def __init__(
    self,
    clientAPIInstance,
    loginSession,
    frequency,
    pageLimit,
    maxRequests,
    pollerQueue
  ):
    super().__init__(sleepTime=0.1, frequency=frequency)
    self.clientAPIInstance=clientAPIInstance
    self.loginSession=loginSession
    self.pageLimit=pageLimit
    self.maxRequests=maxRequests
    self.pollerQueue = pollerQueue

  def worker(self):
    fetchRunning = True
    numRequestsSent = 0
    while fetchRunning:
      numRequestsSent += 1
      remainingMessages = self.requestBatchOfPagesAndReturnRemainingCount()
      if remainingMessages == 0:
        fetchRunning = False
      if numRequestsSent == self.maxRequests:
        fetchRunning = False

  def requestBatchOfPagesAndReturnRemainingCount(self):

    result = self.clientAPIInstance.sendGetRequest(
      url="/consume?limit=" + str(self.pageLimit),
      loginSession=self.loginSession,
      injectHeadersFn=None
    )
    if result.status_code != 200:
      self.clientAPIInstance.raiseResponseException(result)

    remainingMessages = int(result.headers["x-remaining"])

    resultDict = json.loads(result.content)

    for curResult in resultDict:
      self.pollerQueue.put(ChangeNotificationMessage(dict=curResult, clientAPIInstance=self.clientAPIInstance))


    return remainingMessages
