'''
This utility is designed to continously call Ethos API's until it is terminated by keyboard input (ctrl+c)
The reason for this is so that I can test and demo the poller functinoality of the library

It works by continously creating, then deleting person holds.

'''
import time
import sys
import os

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
sys.path.insert(0, os.path.abspath('../'))

import EllucianEthosPythonClient
import queue


#sys.path.insert(0, os.path.abspath('../utils'))
#import Common
#ethosBaseURL = Common.GetFromEnvironment("ETHOSBASEURL")
#ethosAPIKey = Common.GetFromEnvironment("ICETHOSDEVAPIKEY")

ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosAPIKey = os.environ["ICETHOSDEVAPIKEY"]

changeDelayTime = 3

print("Sample Start")

personResourceIDList = [
  "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b",
  "f41aa35d-431e-4301-aa2b-d0799ea53ac5",
  "4c89b26e-8cf9-4697-856f-ab677265b2ce",
  "fb7db2a8-1c79-4d77-8bb7-e54ce202c42b",
  "c4b1718a-3fa8-452d-86cc-92eaa671ae23",
  "6ca9c61b-d441-4d29-befa-d841bf0bc767",
  "4b09bcbd-629b-4e5a-8439-6f1027770f97",
  "7ecdf9a8-5112-475c-99b5-ba3fedc547b6",
  "ac1388f2-a687-4a17-b600-5dace001dbdd",
  "5bcbc3b1-cf8a-4ea6-9042-1dc3e14aa3ba",
  "8c77d8b8-3dd2-4be3-a6b5-2ce6682af310",
  "741cf943-88e8-49e3-85f4-3e90d2e19c40",
  "4b781745-6f0f-47d7-80d8-147d2707222d",
  "f9247aee-a9fe-446e-b01b-a2758f4e1701",
  "93e81e3d-4541-4605-8994-6aa74c7ccd3f",
  "f1d31dd9-b141-4932-a8b6-d09637f1876d",
  "46c03542-9c45-46df-beaa-8db2a09bb460"
]

personHoldCategoryGUID = "45182c89-6bb8-4996-a05a-6fce28f028eb"

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)

def createPersonHoldAndReturnGUID(personGUID):
  personHoldToCreate = {
    'endOn': '2099-12-31T00:00:00Z',
    'person': {'id': personGUID},
    'startOn': '2020-01-17T00:00:00Z',
    'type': {
      'category': 'academic',
      'detail': {
        'id': personHoldCategoryGUID
      }
    }
  }
  createdPersonHold = ethosClient.createResource(
    loginSession=loginSession,
    resourceName="person-holds",
    resourceDict=personHoldToCreate,
    version="6"
  )
  return createdPersonHold.resourceID

def deletePersonHold(personHoldGUID):
  ethosClient.deleteResource(
    loginSession=loginSession,
    resourceName="person-holds",
    resourceID=personHoldGUID
  )


print("Starting to send stream of changes to Ethos API's")
print("Press ctl+c to end")
creating=True
nextPersonIDToUse=0
q = queue.Queue()
try:
  while True:
    if q.empty():
      creating = True
      nextPersonIDToUse = 0
    else:
      if q.qsize()==len(personResourceIDList) :
        creating = False

    if creating:
      personHoldGUID = createPersonHoldAndReturnGUID(personGUID=personResourceIDList[nextPersonIDToUse])
      print("+", end="", flush=True)
      q.put(personHoldGUID)
      nextPersonIDToUse += 1
    else:
      ite = q.get()
      deletePersonHold(ite)
      print("-", end="", flush=True)

    time.sleep(changeDelayTime)
except KeyboardInterrupt:
    print('\nctl+c pressed - so terminating')

print("Deleting any remaing resources")
while not q.empty():
  ite = q.get()
  deletePersonHold(ite)
  print("-", end="", flush=True)

ethosClient.close()


print("\nSample End")
