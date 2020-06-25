from .BaseResourceWrapper import BaseResourceWrapper
import copy

def registerKnownResourses(resoursRegistryDict):
  def getKnownResource(version):
    majorVersion = version.split(".")[0]
    if majorVersion=="6":
      return PersonsV6
    if majorVersion=="8":
      return PersonsV8
    if majorVersion=="12":
      return PersonsV12
    return None
  resoursRegistryDict["persons"]=getKnownResource

class Persons(BaseResourceWrapper):
  addressListCache = None

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def _getDictForPut(self):
    retVal = copy.deepcopy(self.dict)

    #Updating addresses not yet supported
    # sending them to API causes error
    del retVal["addresses"]
    return retVal

  def _afterDictChanged(self):
    self.addressListCache = None

  def getAddresses(self, loginSession):
    if self.addressListCache is None:
      self.addressListCache = []
      for curAddress in self.dict["addresses"]:
        newObj = copy.deepcopy(curAddress)
        newObj["address"] = self.clientAPIInstance.getResource(
          loginSession=loginSession,
          resourceName="addresses",
          resourceID=curAddress["address"]["id"],
          version=None
        )
        self.addressListCache.append(newObj)

    return self.addressListCache

  def getVisas(self, loginSession):
    params = {
      "criteria": "{\"person\": {\"id\": \"" + self.resourceID + "\"}}"
    }
    return self.clientAPIInstance.getResourceIterator(
      loginSession=loginSession,
      resourceName="person-visas",
      version=None,
      params=params,
      pageSize=25
    )

class PersonsV6(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class PersonsV8(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class PersonsV12(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
