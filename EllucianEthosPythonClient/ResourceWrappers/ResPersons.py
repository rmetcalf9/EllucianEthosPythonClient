from .BaseResourceWrapper import BaseResourceWrapper

def registerKnownResourses(resoursRegistryDict):
  resoursRegistryDict["persons"] = {
    6: PersonsV6,
    8: PersonsV8,
    12: PersonsV12
  }

class Persons(BaseResourceWrapper):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class PersonsV6(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class PersonsV8(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class PersonsV12(Persons):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
