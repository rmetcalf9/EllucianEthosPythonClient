


class ListBasedResourceIterator:
  apiClient = None
  loginSession = None
  resourceName = None
  version = None
  resourceIDList = None
  curIdx = None

  def __init__(self, apiClient, loginSession, resourceName, version, resourceIDList):
    self.apiClient = apiClient
    self.loginSession = loginSession
    self.resourceName = resourceName
    self.version = version
    self.resourceIDList = resourceIDList
    self.curIdx = 0

  def __iter__(self):
    self.curIdx = 0
    return self

  def __next__(self):
    if self.curIdx < len(self.resourceIDList):
      retVal = self.apiClient.getResource(
        loginSession=self.loginSession,
        resourceName=self.resourceName,
        resourceID=self.resourceIDList[self.curIdx],
        version=self.version
      )
      self.curIdx += 1
      return retVal

    raise StopIteration
