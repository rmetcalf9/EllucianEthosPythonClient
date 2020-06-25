import sys
import os

# This sample uses a resource iterator to list all the visas for a particular person

import EllucianEthosPythonClient

ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosAppAPIKey = os.environ["ICETHOSDEVAPIKEY"]

personResourceID = "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b"

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAppAPIKey)

print("Start")

print("First obtain the person object")

person = ethosClient.getResource(
  loginSession=loginSession,
  resourceName="persons",
  resourceID=personResourceID,
  version=None
)
print("Found:", person.dict["names"][0]["fullName"])

print("Next list all that persons visas")
cur = 0
for curVisa in person.getVisas(loginSession=loginSession):
  cur += 1
  print(cur, "visa", curVisa.dict)

print("End")
