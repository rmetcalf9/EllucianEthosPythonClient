
import os
import sys
import Common

##https://resources.elluciancloud.com/bundle/person-holds/page/6.0/index.html

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
sys.path.insert(0, os.path.abspath('../'))
import EllucianEthosPythonClient

ethosBaseURL = Common.GetFromEnvironment("ETHOSBASEURL")
ethosAPIKey = Common.GetFromEnvironment("ICETHOSDEVAPIKEY")

personResourceID = "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b"
personHoldCategoryGUID = "45182c89-6bb8-4996-a05a-6fce28f028eb"

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)

personHoldIterator = ethosClient.getResourceIterator(
  loginSession=loginSession,
  resourceName="person-holds",
  version=None,
  pageSize=9
)

max = 13
cur = 0
for personHold in personHoldIterator:
  #print("personHold", personHold.dict["person"]["id"], personHold.dict["startOn"])
  print("personHold", personHold.dict)
  cur += 1
  if cur > max:
    break

print("Iterator run so now creating a person-hold")

personHoldToCreate = {
    'endOn': '2099-12-31T00:00:00Z',
    'person': {'id': personResourceID},
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

print("Created a new person-hold resource with id ", createdPersonHold.version)
print("GUID of returned resource ", createdPersonHold.resourceID)

print("Deleting using obj method")
createdPersonHold.delete(loginSession=loginSession)

print("Creating another person hold so it can be deleted using id only")
createdPersonHold = ethosClient.createResource(
  loginSession=loginSession,
  resourceName="person-holds",
  resourceDict=personHoldToCreate,
  version="6"
)

print("Created a new person-hold resource with id ", createdPersonHold.version)
print("GUID of returned resource ", createdPersonHold.resourceID)

print("Deleting using obj method")
ethosClient.deleteResource(
  loginSession=loginSession,
  resourceName="person-holds",
  resourceID=createdPersonHold.resourceID
)


print("End")
