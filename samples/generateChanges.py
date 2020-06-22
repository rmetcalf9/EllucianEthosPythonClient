'''
This utility is designed to continously call Ethos API's until it is terminated by keyboard input (ctrl+c)
The reason for this is so that I can test and demo the poller functinoality of the library

It works by continously creating, then deleting person holds.

'''
import time
import sys
import os
sys.path.insert(0, os.path.abspath('../'))
import EllucianEthosPythonClient


#sys.path.insert(0, os.path.abspath('../utils'))
#import Common
#ethosBaseURL = Common.GetFromEnvironment("ETHOSBASEURL")
#ethosAPIKey = Common.GetFromEnvironment("ICETHOSDEVAPIKEY")

ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosAPIKey = os.environ["ICETHOSDEVAPIKEY"]


print("Sample Start")

personResourceIDList = [
  "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b"
]
personHoldCategoryGUID = "45182c89-6bb8-4996-a05a-6fce28f028eb"

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)


print("Starting to send stream of changes to Ethos API's")
print("Press ctl+c to end")
try:
  while True:
    print(".", end="", flush=True)
    time.sleep(0.5)
except KeyboardInterrupt:
    print('\nctl+c pressed - so terminating')


print("Sample End")
