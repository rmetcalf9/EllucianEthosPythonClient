import os
import sys
import Common

sys.path.insert(0, os.path.abspath('../'))
import EllucianEthosPythonClient

print("Using EllucianEthosPythonClient version", EllucianEthosPythonClient.__version__)

ethosBaseURL = Common.GetFromEnvironment("ETHOSBASEURL")
ethosAPIKey = Common.GetFromEnvironment("ICETHOSDEVAPIKEY")

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)

loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)

ethosClient.getResource(
  loginSession=loginSession,
  resourceName="persons",
  resourceID="ddd"
)
