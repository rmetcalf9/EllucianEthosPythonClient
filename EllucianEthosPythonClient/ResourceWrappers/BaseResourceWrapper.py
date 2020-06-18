
class BaseResourceWrapper():
  clientAPIInstance = None
  dict = None
  version = None
  resourseName = None
  def __init__(self, clientAPIInstance, dict, version, resourseName):
    self.clientAPIInstance = clientAPIInstance
    self.dict = dict
    self.version = version
    self.resourseName = resourseName

