# Utility used to call API and generate mock data.
#  the mock data can then be inserted into the tests

import os
import sys
import Common
import json

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
personHoldResourceID = "0e1f48c4-5669-4a94-92ad-d64d37af811a"

ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)

loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)

testRequests = {}
testRequests["getSinglePerson"] = {
  "url": "/api/persons/" + personResourceID,
  "method": "get",
  "postData": None
}
testRequests["getPersonHold"] = {
  "url": "/api/person-holds/" + personHoldResourceID,
  "method": "get",
  "postData": None
}
testRequests["consumeChangeNotification"] = {
  "url": "/consume?limit=20",
  "method": "get",
  "postData": None
}

requestToTest = testRequests["consumeChangeNotification"]

(result, sendingNoneData) = Common.executeAPICall(api=ethosClient, loginSession=loginSession, requestToTest=requestToTest)


print("Response status_code was:" + str(result.status_code))
print("Response headers were:" + str(result.headers))
print("Response contentDict was:" + result.content.decode("utf-8"))


if sendingNoneData:
  print("data=None")
else:
  print("data=DDD")
  raise Exception("Not Implemented")
print("#response=base64.b64encode(json.dumps({")
print("#  ##TODO")
print("#}).encode(\"UTF-8\")")
print("response=" + str(result.content))
print("mock.registerNextResponse(")
print("  reqFnName=\"get\",")
print("  url=\"" + requestToTest["url"] + "\",")
print("  data=data,")
print("  status_code=200,")
print("  contentBytes=base64.b64encode(json.dumps(response)),")
print("  ignoreData=False")
print(")")

print("Code END ----------------------")


