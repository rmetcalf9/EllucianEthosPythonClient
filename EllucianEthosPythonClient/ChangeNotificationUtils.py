from .ChangeNotificationMessage import ChangeNotificationMessage
import json


def requestBatchOfPagesAndReturnRemainingCountLib(
  pageLimit,
  lastProcessedID,
  clientAPIInstance,
  loginSession,
  processIndividualMessage
):
  params = {
    "limit": str(pageLimit)
  }
  if lastProcessedID is not None:
    params["lastProcessedID"] = lastProcessedID
  result = clientAPIInstance.sendGetRequest(
    url="/consume",
    params=params,
    loginSession=loginSession,
    injectHeadersFn=None
  )
  if result.status_code != 200:
    clientAPIInstance.raiseResponseException(result)

  remainingMessages = int(result.headers["x-remaining"])
  resultDict = json.loads(result.content)

  for curResult in resultDict:
    changeNotification = ChangeNotificationMessage(dict=curResult, clientAPIInstance=clientAPIInstance)
    processIndividualMessage(changeNotification=changeNotification)

  return remainingMessages

class ChangeNotificationIterator:
  clientAPIInstance = None
  loginSession = None
  pageLimit = None
  maxRequests = None

  requestsRemaining = None
  curIdx = None
  curResultList = None

  def __init__(self, loginSession, pageLimit, maxRequests, clientAPIInstance):
    self.clientAPIInstance = clientAPIInstance
    self.loginSession = loginSession
    self.pageLimit = pageLimit
    self.maxRequests = maxRequests

    self.requestsRemaining = self.maxRequests
    self.curIdx = 0
    self.curResultList = []

  def __iter__(self):
    self.requestsRemaining = self.maxRequests
    self.curIdx = 0
    self.curResultList = []
    return self

  def loadNewPageOfResults(self):
    self.curIdx = 0
    self.curResultList = []

    def processIndividualMessage(changeNotification):
      self.curResultList.append(changeNotification)

    requestBatchOfPagesAndReturnRemainingCountLib(
      pageLimit=self.pageLimit,
      clientAPIInstance=self.clientAPIInstance,
      loginSession=self.loginSession,
      processIndividualMessage=processIndividualMessage,
      lastProcessedID=None
    )

  def __next__(self):
    if self.curIdx >= len(self.curResultList):
      if self.requestsRemaining==0:
        raise StopIteration
      self.requestsRemaining -= 1
      self.loadNewPageOfResults()

    if self.curIdx >= len(self.curResultList):
      # We tried getting a new page but there are still not results
      # so terminate
      raise StopIteration

    retVal = self.curResultList[self.curIdx]
    self.curIdx += 1
    return retVal
