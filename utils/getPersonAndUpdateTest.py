# Simple utility to use API to retrieve a person

import os
import sys
import Common

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
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
  resourceID=personResourceID,
  version="12"
)

print("Person Type Object=", type(person).__name__)
print("Person Type ID=", person.resourceID)
print("Person Retrieved lastName=", person.dict["names"][0]["lastName"])
input("Press Enter to continue and update or ctrl+c to quit...")

#Known issue - See and error AddressLine is required
# - it might be that person needs to load all the addresses as well in order to save any change sucessfully

person.dict["names"][0]["lastName"] = person.dict["names"][0]["lastName"] + "x"
print("Trying to change lastName to=", person.dict["names"][0]["lastName"])

person.save(loginSession=loginSession)

print("Name in obj after put sent=", person.dict["names"][0]["lastName"])
