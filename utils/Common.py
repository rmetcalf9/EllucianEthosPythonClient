# Common functions used in utils
import os

def GetFromEnvironment(environVariable):
  if environVariable in os.environ:
    return os.environ[environVariable]
  raise Exception("Could not find " + environVariable + " in envionment for testing")


def executeAPICall(api, loginSession, requestToTest):
  sendingNoneData = False
  if requestToTest["method"] == "get":
    sendingNoneData = True
    result = api.sendGetRequest(
      loginSession=loginSession,
      url=requestToTest["url"]
    )
  if requestToTest["method"] == "post":
    result = api.sendPostRequest(
      loginSession=loginSession,
      url=requestToTest["url"],
      data=json.dumps(requestToTest["postData"])
    )
  return (result, sendingNoneData)