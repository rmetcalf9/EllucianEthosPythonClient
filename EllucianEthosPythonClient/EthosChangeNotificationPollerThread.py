from .WorkerThread import WorkerThread

class EthosChangeNotificationPollerThreadExceptionClass(Exception):
  pass

class EthosChangeNotificationPollerThread(WorkerThread):
  clientAPIInstance = None
  loginSession = None
  pageSize = None
  maxRequests = None

  def __init__(
    self,
    clientAPIInstance,
    loginSession,
    frequency,
    pageSize,
    maxRequests
  ):
    super().__init__(sleepTime=0.1, frequency=frequency)
    self.clientAPIInstance=clientAPIInstance
    self.loginSession=loginSession
    self.pageSize=pageSize
    self.maxRequests=maxRequests


