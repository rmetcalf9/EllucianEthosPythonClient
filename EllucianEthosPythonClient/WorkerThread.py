import threading
import time
import datetime
import pytz

class WorkerThreadExceptionClass(Exception):
  pass

#First impleimentaion was using pref_counter
# reimplemented to use date time due to limitations
def getNextWorkerTime(lastRunTime, curTime, frequency):
  retVal = lastRunTime
  while retVal < curTime:
    retVal = retVal + datetime.timedelta(seconds=int(frequency))
  return retVal


class WorkerThread(threading.Thread):
  sleepTime = None
  running = None
  stopped = None
  thrownException = None
  frequency = None

  nextWorkerTime = None

  def __init__(self, sleepTime, frequency):
    super().__init__()
    self.sleepTime = sleepTime
    self.running = False
    self.thrownException = None
    self.stopped = False
    self.frequency=frequency

    #First run is immediately when thread is started
    self.nextWorkerTime = datetime.datetime.now(pytz.timezone("UTC"))

  def run(self):
    try:
      self.stopped=False
      self.running = True
      while self.running:
        #now = datetime.datetime.now(pytz.timezone("UTC"))
        if datetime.datetime.now(pytz.timezone("UTC")) > self.nextWorkerTime:
          self.worker()
          self.nextWorkerTime = getNextWorkerTime(
            lastRunTime=self.nextWorkerTime,
            curTime=datetime.datetime.now(pytz.timezone("UTC")),
            frequency=self.frequency
          )
        time.sleep(self.sleepTime)
      self.stopped=True
    except Exception as Excep:
      self.thrownException = WorkerThreadExceptionClass("Poller thread threw an exception - " +  str(Excep))
      self.running = False

  def close(self, wait=True):
    if self.stopped:
      raise WorkerThreadExceptionClass("Should not try to close thread twice")
    self.stopped = False
    self.running = False
    if wait:
      while self.stopped == False:
        self.healthCheck()
        time.sleep(self.sleepTime)

  def healthCheck(self):
    #Run in controller thread to raise any exceptions
    if self.running:
      if not self.isAlive():
        raise WorkerThreadExceptionClass("Poller thread is no longer alive")
    if self.thrownException is not None:
      raise self.thrownException

  def worker(self):
    pass #shuold be overridden