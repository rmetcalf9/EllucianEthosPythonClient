# Simple example that uses the poller
# This is a simple non-reliable implementation. All messages will be taken off the queue no matter if they are
# sucessfully processed or not.
import sys
import os

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
##sys.path.insert(0, os.path.abspath('../'))

import EllucianEthosPythonClient
import queue
import time

ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosPollerAppAPIKey = os.environ["ETHOSPOLLERAPIKEY"]
##ethosPollerAppAPIKey = os.environ["ICETHOSDEVAPIKEY"]


lastprocessid_FileName = "./pollerguideTempFileForLastProcessedID.txt"

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosPollerAppAPIKey)


def processSingleMessage(apiClient, messageid, changeNotification):
  # in a real example this part would write to file or update a db
  ##print("received ", changeNotification.operation, changeNotification.resourceName, changeNotification.resourceID)
  with open(lastprocessid_FileName, 'w') as filetowrite:
    filetowrite.write(messageid)
  return True

print("Start")


print("Reading lastprocessedid from file")
lastProcessedID=""
with open(lastprocessid_FileName, 'r') as filetowrite:
    lastProcessedID=filetowrite.read()
print(" - lastProcessedID", lastProcessedID)

print("Starting receive thread")
ethosClient.startChangeNotificationPollerThreadInFunctionMode(
  loginSession=loginSession,
  frequency=10,  # number of seconds between fetches
  pageLimit=20,  # number of change notifications to get per requests
  maxRequests=4,  # maximum number of rquests to use in each fecth
  lastProcessedID=lastProcessedID,
  messageProcessingFunction=processSingleMessage
)

print("Main loop - ctl+c to terminate")
try:
  while True:
    ethosClient.healthCheck() # detects is thread has died and if so raises an exception
    time.sleep(0.5)
except KeyboardInterrupt:
    print('\nctl+c pressed - so terminating')

ethosClient.close()

print("End")