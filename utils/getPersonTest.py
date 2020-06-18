import os
import sys
import Common

sys.path.insert(0, os.path.abspath('../'))
import EllucianEthosPythonClient

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
print(person.dict)

print("Person Retrieved=", person)