from .BaseResourceWrapper import BaseResourceWrapper
import copy

def registerKnownResourses(resoursRegistryDict):
  resoursRegistryDict["persons"] = {
    "6": PersonsV6,
    "8": PersonsV8,
    "12": PersonsV12,
    "12.1.0": PersonsV12
  }

class Persons(BaseResourceWrapper):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def _getDictForPut(self):
    retVal = copy.deepcopy(self.dict)

    #Updating addresses not yet supported
    # sending them to API causes error
    del retVal["addresses"]
    return retVal

class PersonsV6(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class PersonsV8(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class PersonsV12(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
