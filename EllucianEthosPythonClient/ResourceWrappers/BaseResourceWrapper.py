
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

    if "id" not in dict:
      raise Exception("Invalid resource dict (missing id)")
    if not isinstance(version , str):
      raise Exception("Version passed must be a string")

    self.resourceID = dict["id"]

