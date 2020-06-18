# Simple utility to use API to retrieve a person

import os
import sys
import Common

sys.path.insert(0, os.path.abspath('../'))
import EllucianEthosPythonClient

# If the __version__ contains dirty it means we are using the library from the code
#  rather than a pip installed version
print("Using EllucianEthosPythonClient version", EllucianEthosPythonClient.__version__)

ethosBaseURL = Common.GetFromEnvironment("ETHOSBASEURL")
ethosAPIKey = Common.GetFromEnvironment("ICETHOSDEVAPIKEY")

personResourceID = "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b"

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)

loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)

person = ethosClient.getResource(
  loginSession=loginSession,
  resourceName="persons",
  resourceID=personResourceID
)

print("Person Type Object=", type(person).__name__)
print("Person Retrieved=", person.dict["names"][0]["fullName"])
