from .APIClients import APIClientBase
from .EthosLoginSession import EthosLoginSessionBasedOnAPIKey
from .ResourceWrappers import getResourceWrapper
from .ResourceIterator import ResourceIterator
from .ListBasedResourceIterator import ListBasedResourceIterator
from .ChangeNotificationUtils import ChangeNotificationIterator
from .EthosChangeNotificationPollerThread import EthosChangeNotificationPollerThreadQueueMode, EthosChangeNotificationPollerThreadFunctionMode
import json

class CanNotStartChangeNotificationPollerTwiceException(Exception):
  pass

class EllucianEthosAPIClient(APIClientBase):
  refreshAuthTokenIfRequired = None
  changeNotificationPollerThread = None

  def __init__(self, baseURL, mock=None):
    super().__init__(baseURL=baseURL, mock=mock, forceOneRequestAtATime=True)
    self.changeNotificationPollerThread = None

  def getLoginSessionFromAPIKey(self, apiKey):
    return EthosLoginSessionBasedOnAPIKey(APIClient=self, apikey=apiKey)

  def _getResourceRAW(self, loginSession, resourceName, resourceID, version=None):
    #print("_getResourceRAW", resourceName, resourceID, version)

    def injectHeaderFN(headers):
      if version is not None:
        headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"

    result = self.sendGetRequest(
      url="/api/" + resourceName + "/" + resourceID,
      loginSession=loginSession,
      injectHeadersFn=injectHeaderFN
    )
    if result.status_code == 404:
      return (None, None, None)
    if result.status_code != 200:
      self.raiseResponseException(result)

    versionReturned = self.getVersionIntFromHeader(result.headers["x-hedtech-media-type"])
    return (result.content, versionReturned, resourceName)

  #Doc list https://xedocs.ellucian.com/xe-banner-api/ethos_apis/foundation/persons/person_get_guid_v6.html
  def getResource(self, loginSession, resourceName, resourceID, version=None):
    (resultContent, versionReturned, resourceName) = self._getResourceRAW(loginSession=loginSession, resourceName=resourceName, resourceID=resourceID, version=version)
    if resultContent is None:
      return None
    return getResourceWrapper(clientAPIInstance=self, dict=json.loads(resultContent), version=versionReturned, resourseName=resourceName)

  def getResourceIterator(self, loginSession, resourceName, version=None, pageSize=25, params=None):
    return ResourceIterator(self, loginSession, resourceName, version, pageSize, params=params)

  def getListBasedResourceIterator(self, loginSession, resourceName, resourceIDList, version=None):
    return ListBasedResourceIterator(self, loginSession, resourceName, version, resourceIDList=resourceIDList)

  def getChangeNotificationIterator(self, loginSession, pageLimit=25, maxRequests=4):
    return ChangeNotificationIterator(
      loginSession=loginSession,
      pageLimit=pageLimit,
      maxRequests=maxRequests,
      clientAPIInstance=self
    )

  def getVersionIntFromHeader(self, meaidTypeHeaderValue):
    #example: application/vnd.hedtech.integration.v6+json
    requiredStart = "application/vnd.hedtech.integration.v"
    requiredEnd = "+json"
    if not meaidTypeHeaderValue.startswith(requiredStart):
      raise Exception("Could not determine resource version")
    meaidTypeHeaderValue = meaidTypeHeaderValue[len(requiredStart):]
    if not meaidTypeHeaderValue.endswith(requiredEnd):
      raise Exception("Could not determine resource version - header didn't end with " + requiredEnd)
    meaidTypeHeaderValue = meaidTypeHeaderValue[:-len(requiredEnd)]
    return meaidTypeHeaderValue

  def createResource(
    self,
    loginSession,
    resourceName,
    resourceDict,
    version=None
  ):
    if version is None:
      raise Exception("Must supply version when creating resource")
    def injectHeaderFN(headers):
        headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"
        headers["Content-Type"] = "application/vnd.hedtech.integration.v" + version + "+json"

    result = self.sendPostRequest(
      url="/api/" + resourceName,
      loginSession=loginSession,
      injectHeadersFn=injectHeaderFN,
      data=json.dumps(resourceDict)
    )
    if result.status_code != 201:
      self.raiseResponseException(result)

    versionReturned = self.getVersionIntFromHeader(result.headers["x-hedtech-media-type"])

    return getResourceWrapper(clientAPIInstance=self, dict=json.loads(result.content), version=versionReturned, resourseName=resourceName)

  def deleteResource(
    self,
    loginSession,
    resourceName,
    resourceID
  ):
    url = "/api/" + resourceName + "/" + resourceID

    result = self.sendDeleteRequest(
      url=url,
      loginSession=loginSession,
      injectHeadersFn=None
    )
    if result.status_code != 200:
      self.raiseResponseException(result)

  def startChangeNotificationPollerThread(
    self,
    loginSession,
    frequency, #number of seconds between fetches
    pageLimit, #number of change notifications to get per requests
    maxRequests, #maximum number of rquests to use in each fecth
    pollerQueue
  ):
    if self.changeNotificationPollerThread is not None:
      raise CanNotStartChangeNotificationPollerTwiceException()
    self.changeNotificationPollerThread = EthosChangeNotificationPollerThreadQueueMode(
      clientAPIInstance=self,
      loginSession=loginSession,
      frequency=frequency,
      pageLimit=pageLimit,
      maxRequests=maxRequests,
      pollerQueue=pollerQueue
    )
    self.changeNotificationPollerThread.start()

  def startChangeNotificationPollerThreadInFunctionMode(
    self,
    loginSession,
    frequency,  # number of seconds between fetches
    pageLimit,  # number of change notifications to get per requests
    maxRequests,  # maximum number of rquests to use in each fecth
    lastProcessedID,
    messageProcessingFunction
  ):
    if self.changeNotificationPollerThread is not None:
      raise CanNotStartChangeNotificationPollerTwiceException()
    self.changeNotificationPollerThread = EthosChangeNotificationPollerThreadFunctionMode(
      clientAPIInstance=self,
      loginSession=loginSession,
      frequency=frequency,
      pageLimit=pageLimit,
      maxRequests=maxRequests,
      lastProcessedID=lastProcessedID,
      messageProcessingFunction=messageProcessingFunction
    )
    self.changeNotificationPollerThread.start()

  def healthCheck(self):
    if self.changeNotificationPollerThread is not None:
      self.changeNotificationPollerThread.healthCheck()

  def close(self):
    if self.changeNotificationPollerThread is not None:
      self.changeNotificationPollerThread.close()
      self.changeNotificationPollerThread = None
