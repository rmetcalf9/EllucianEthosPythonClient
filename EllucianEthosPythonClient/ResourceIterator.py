import json
from .ResourceWrappers import getResourceWrapper

class ResourceIterator:
  apiClient = None
  loginSession = None
  resourceName = None
  version = None
  pageSize = None
  curList = None
  curIdx = None
  curOffset = None
  versionReturned = None
  params = None

  def __init__(self, apiClient, loginSession, resourceName, version, pageSize, params):
    self.apiClient = apiClient
    self.loginSession = loginSession
    self.resourceName = resourceName
    self.version = version
    self.pageSize = pageSize

    self.curList = []
    self.curIdx = 0
    self.curOffset = 0

    if params is None:
      self.params = {}
    else:
      self.params = params

    self.versionReturned = None

  def __iter__(self):
    self.curList = []
    self.curIdx = 0
    self.curOffset = 0
    return self

  def __next__(self):
    if self.curIdx >= len(self.curList):
      self.collectNextPage()
      if self.curIdx >= len(self.curList):
        raise StopIteration
    cur = self.curIdx
    self.curIdx += 1
    return getResourceWrapper(clientAPIInstance=self, dict=self.curList[cur], version=self.versionReturned,resourseName=self.resourceName)

  def collectNextPage(self):
    def injectHeaderFN(headers):
      if self.version is not None:
        headers["Accept"] = "application/vnd.hedtech.integration.v" + self.version + "+json"

    self.params["limit"] = str(self.pageSize)
    self.params["offset"] = str(self.curOffset)
    result = self.apiClient.sendGetRequest(
      url="/api/" + self.resourceName,
      params=self.params,
      loginSession=self.loginSession,
      injectHeadersFn=injectHeaderFN
    )
    if result.status_code != 200:
      self.apiClient.raiseResponseException(result)

    if self.versionReturned is None:
      self.versionReturned = self.apiClient.getVersionIntFromHeader(result.headers["x-hedtech-media-type"])

    self.curList = json.loads(result.content)
    self.curIdx = 0
    self.curOffset += len(self.curList)

