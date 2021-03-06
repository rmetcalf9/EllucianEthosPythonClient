import sys
import os

# This sample uses a resource iterator to list all the visas for a particular person

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
sys.path.insert(0, os.path.abspath('../'))

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

print("Next list all the persons addresses")
cur = 0
for curAddress in person.getAddresses(loginSession=loginSession):
  cur += 1
  print(cur, "address", curAddress)
  print(cur, "address", curAddress["address"].dict)

print("End")
