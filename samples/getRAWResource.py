# This sample shows calling the API directly without trying to cast it to an object

import sys
import os

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
sys.path.insert(0, os.path.abspath('../'))

import EllucianEthosPythonClient

ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosPollerAppAPIKey = os.environ["ETHOSPOLLERAPIKEY"]

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosPollerAppAPIKey)

print("Start")

resourceToFetch="sections"
resourceGUID = "fe524551-f02a-4297-9373-0b9f9bf120c2"
version = None #"16"


exampleURL = "/api/" + resourceToFetch + "/" + resourceGUID

def sampleInjectHeaderFunctionForGet(headers):
  if version is not None:
    headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"

result = ethosClient.sendGetRequest(
  url=exampleURL,
  loginSession=loginSession,
  injectHeadersFn=sampleInjectHeaderFunctionForGet
)

print(result.status_code)
print(result.content)

print("End")
