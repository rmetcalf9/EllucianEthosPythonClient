import json
import copy

NO_ID_IN_DICT = "NO_ID_IN_DICT"

class BaseResourceWrapper():
  clientAPIInstance = None
  dict = None
  version = None
  resourceName = None
  resourceID = None
  def __init__(self, clientAPIInstance, dict, version, resourceName):
    self.clientAPIInstance = clientAPIInstance
    self.dict = dict
    self.version = version
    self.resourceName = resourceName
    if not isinstance(version , str):
      raise Exception("Version passed must be a string")
    self.resourceID = self._getResourceIDFromDict(dict)
    self._afterDictChanged()

  def _getResourceIDFromDict(self, dict):
    if "id" in dict:
      return dict["id"]
    if "guid" in dict:
      return dict["guid"]
    return NO_ID_IN_DICT
    #raise Exception("Invalid resource dict (missing id)")

  def getMajorVersion(self):
    return self.version.split(".")[0]

  def _getDictForPut(self):
    return copy.deepcopy(self.dict)

  def save(self, loginSession):
    if self.resourceID == NO_ID_IN_DICT:
      raise Exception("Can not save - no id in dict")
    def injectHeaderFN(headers):
      headers["Accept"] = "application/vnd.hedtech.integration.v" + self.getMajorVersion() + "+json"
      headers["Content-Type"] = "application/vnd.hedtech.integration.v" + self.getMajorVersion() + "+json"
      ##print(headers)

    url = "/api/" + self.resourceName + "/" + self.resourceID

    result = self.clientAPIInstance.sendPutRequest(
      url=url,
      loginSession=loginSession,
      injectHeadersFn=injectHeaderFN,
      data=json.dumps(self._getDictForPut())
    )
    if result.status_code != 200:
      self.clientAPIInstance.raiseResponseException(result)

    self.dict = json.loads(result.content)
    self._afterDictChanged()

  def delete(self, loginSession):
    if self.resourceID == NO_ID_IN_DICT:
      raise Exception("Can not delete - no id in dict")

    url = "/api/" + self.resourceName + "/" + self.resourceID

    result = self.clientAPIInstance.sendDeleteRequest(
      url=url,
      loginSession=loginSession,
      injectHeadersFn=None,
    )
    if result.status_code != 200:
      self.clientAPIInstance.raiseResponseException(result)

  def refresh(self, loginSession):
    if self.resourceID == NO_ID_IN_DICT:
      raise Exception("Can not refresh - no id in dict")

    (resultContent, versionReturned, resourceName) = self.clientAPIInstance._getResourceRAW(
      loginSession=loginSession,
      resourceName=self.resourceName,
      resourceID=self.resourceID,
      version=self.version
    )
    if versionReturned is None:
      raise Exception("Refresh failed - no resource found")
    if versionReturned != self.version:
      raise Exception("Internal Error wrong version on refresh")
    if resourceName != self.resourceName:
      raise Exception("Internal Error wrong resourceName on refresh")
    self.dict = json.loads(resultContent)
    self._afterDictChanged()

  def _afterDictChanged(self):
    # called after the dict changes e.g. creation and refresh
    #  allows sub classes to remove caches
    pass