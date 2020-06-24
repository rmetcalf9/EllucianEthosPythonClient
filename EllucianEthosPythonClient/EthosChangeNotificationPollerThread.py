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
  lastProcessedID = None

  def __init__(
    self,
    clientAPIInstance,
    loginSession,
    frequency,
    pageLimit,
    maxRequests,
    lastProcessedID
  ):
    super().__init__(sleepTime=0.1, frequency=frequency)
    self.clientAPIInstance=clientAPIInstance
    self.loginSession=loginSession
    self.pageLimit=pageLimit
    self.maxRequests=maxRequests
    self.lastProcessedID = lastProcessedID

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
    url = "/consume?limit=" + str(self.pageLimit)
    if self.lastProcessedID is not None:
      url += "&lastProcessedID=" + self.lastProcessedID
    result = self.clientAPIInstance.sendGetRequest(
      url=url,
      loginSession=self.loginSession,
      injectHeadersFn=None
    )
    if result.status_code != 200:
      self.clientAPIInstance.raiseResponseException(result)

    remainingMessages = int(result.headers["x-remaining"])
    resultDict = json.loads(result.content)

    for curResult in resultDict:
      changeNotification = ChangeNotificationMessage(dict=curResult, clientAPIInstance=self.clientAPIInstance)
      self.processMessage(changeNotification=changeNotification)
      if self.lastProcessedID is not None:
        self.lastProcessedID = changeNotification.messageID

    return remainingMessages

  def processMessage(self, changeNotification):
    pass


class EthosChangeNotificationPollerThreadQueueMode(EthosChangeNotificationPollerThread):
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
    super().__init__(
      clientAPIInstance=clientAPIInstance,
      loginSession=loginSession,
      frequency=frequency,
      pageLimit=pageLimit,
      maxRequests=maxRequests,
      lastProcessedID=None
    )
    self.pollerQueue = pollerQueue

  def processMessage(self, changeNotification):
    self.pollerQueue.put(changeNotification)

class EthosChangeNotificationPollerThreadFunctionMode(EthosChangeNotificationPollerThread):
  messageProcessingFunction = None

  def __init__(
    self,
    clientAPIInstance,
    loginSession,
    frequency,
    pageLimit,
    maxRequests,
    lastProcessedID,
    messageProcessingFunction
  ):
    super().__init__(
      clientAPIInstance=clientAPIInstance,
      loginSession=loginSession,
      frequency=frequency,
      pageLimit=pageLimit,
      maxRequests=maxRequests,
      lastProcessedID=lastProcessedID
    )
    self.messageProcessingFunction = messageProcessingFunction

  def processMessage(self, changeNotification):
    self.messageProcessingFunction(apiClient=self.clientAPIInstance, messageid=changeNotification.messageID, changeNotification=changeNotification)
