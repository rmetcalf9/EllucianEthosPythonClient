
import os
import sys
import Common

##https://resources.elluciancloud.com/bundle/person-holds/page/6.0/index.html

sys.path.insert(0, os.path.abspath('../'))
import EllucianEthosPythonClient

ethosBaseURL = Common.GetFromEnvironment("ETHOSBASEURL")
ethosAPIKey = Common.GetFromEnvironment("ICETHOSDEVAPIKEY")

personResourceID = "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b"

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)

personHoldIterator = ethosClient.getResourceIterator(
  loginSession=loginSession,
  resourceName="person-holds",
  version=None
)

max = 123
cur = 0
for personHold in personHoldIterator:
  print("personHold", personHold.dict["person"]["id"], personHold.dict["startOn"])
  cur += 1
  if cur > max:
    break

print("End")
