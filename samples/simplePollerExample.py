# Simple example that uses the poller
# This is a simple non-reliable implementation. All messages will be taken off the queue no matter if they are
# sucessfully processed or not.
import sys
import os

import EllucianEthosPythonClient
import queue
import time

ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosPollerAppAPIKey = os.environ["ETHOSPOLLERAPIKEY"]
##ethosPollerAppAPIKey = os.environ["ICETHOSDEVAPIKEY"]


print("Start")

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosPollerAppAPIKey)


changeNotificationQueue = queue.Queue()
ethosClient.startChangeNotificationPollerThread(
  loginSession=loginSession,
  frequency=10,  # number of seconds between fetches
  pageLimit=20,  # number of change notifications to get per requests
  maxRequests=4,  # maximum number of rquests to use in each fecth
  pollerQueue=changeNotificationQueue
)

print("Starting to watch for messages - ctl+c to terminate")
try:
  while True:
    while changeNotificationQueue.qsize()>0:
      changeNotification = changeNotificationQueue.get()
      print("Recieved", changeNotification.operation, changeNotification.resourceName, changeNotification.resourceID, changeNotification.resourceWrapper)

    ethosClient.healthCheck() # detects is thread has died and if so raises an exception
    time.sleep(0.5)
except KeyboardInterrupt:
    print('\nctl+c pressed - so terminating')


ethosClient.close()

print("End")