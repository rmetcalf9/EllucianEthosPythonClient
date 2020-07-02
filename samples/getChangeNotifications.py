import sys
import os

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
sys.path.insert(0, os.path.abspath('../'))

import EllucianEthosPythonClient

ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosPollerAppAPIKey = os.environ["ETHOSPOLLERAPIKEY"]

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosPollerAppAPIKey)

print("Start")

changeNotificationIterator = ethosClient.getChangeNotificationIterator(
  loginSession=loginSession,
  pageLimit=20,
  maxRequests=4
)


numNotifications = 0
for curChangeNotification in changeNotificationIterator:
  numNotifications += 1
  print(curChangeNotification.getSimpleDict())

print("End num notifications received:", numNotifications)
