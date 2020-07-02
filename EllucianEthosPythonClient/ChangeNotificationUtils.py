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