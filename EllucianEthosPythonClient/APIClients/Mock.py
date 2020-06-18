from builtins import list

from requests.models import Response
import base64
import json
import copy

# import python_Testing_Utilities
# In future I want a function like this in python_Testing_Utilities to give a good comparison of dicts
# def dictDifferenceString(
#           dictAName,
#           dictA,
#           dictBName,
#           dictB,
#           maxRecurse=3
#         ):
#   if maxRecurse==0:
#     return "Recurse limit reached\n"
#   aKeys = list(dictA.keys())
#   bKeys = list(dictB.keys())
#   if not python_Testing_Utilities.objectsEqual(aKeys, bKeys):
#     ret = "Keys mismatch\n"
#     ret += dictAName + ":" + str(aKeys) + "\n"
#     ret += dictBName + ":" + str(bKeys) + "\n"
#     return ret
#   # #list(dictA.keys()) == list(dictB.keys())
#   ret = ""
#   for curKey in aKeys:
#     try:
#       ret += "****" + str(dictB[curKey])  + "\n"
#       if not python_Testing_Utilities.objectsEqual(dictA[curKey],dictB[curKey]):
#         ret += dictAName + "." + curKey + " is not equal to " + dictBName + "." + curKey + "\n"
#     except Exception as err:
#       ret += str(err) + "\n"
#   return ret


class mockRequestClass():
  method = None
  url = None
  def __init__(self, method, url):
    self.method = method
    self.url = url

class ExpectedResult():
  reqFnName = None
  url = None
  data = None
  ignoreData = None
  def __init__(self, reqFnName, url, data, response=None, ignoreData=False):
    self.reqFnName = reqFnName
    self.url = url
    self.data = data
    self.response = response
    self.ignoreData = ignoreData

  def __str__(self):
    return  self.reqFnName + "->" + self.url

  def requestMatches(self, reqFnName, url, data):
    if self.reqFnName != reqFnName:
      return False
    if self.url != url:
      return False
    if self.ignoreData:
      return True
    if self.data != data:
      return False
    return True

  def getResponse(self):
    return self.response




class MockNoResultSetupException(Exception):
  recievedRequest = None
  def __init__(self, recievedRequest):
    self.recievedRequest = recievedRequest

  def __str__(self):
    return "NoMockResultsSetupException - " + str(self.recievedRequest)

class MockIncorrectResultException(Exception):
  recievedRequest = None
  expectedResult = None
  recievedData = None
  def __init__(self, recievedRequest, expectedResult, recievedData):
    self.recievedRequest = recievedRequest
    self.expectedResult = expectedResult
    self.recievedData = recievedData

  def isStrValidDICT(self, data):
    if not isinstance(data, str):
      return False
    try:
      x = json.loads(data)
      return True
    except Exception as exp:
      return False

  def __str__(self):
    if str(self.recievedRequest) == str(self.expectedResult):
      ret = "\n*******************************************\n"
      ret += "Request " + str(self.recievedRequest) + "\n"
      jsonComparison = False
      if self.isStrValidDICT(self.expectedResult.data):
        if self.isStrValidDICT(self.recievedData):
          jsonComparison = True
      ret += "Got Data:" + str(self.recievedData) + "\n\n"
      ret += "Expected Data:" + str(self.expectedResult.data) + "\n"
      if jsonComparison:
        ret += "Both results are valid json\n"
        # ret += dictDifferenceString(
        #   dictAName="GOT",
        #   dictA=json.loads(self.recievedData),
        #   dictBName="EXPECTED",
        #   dictB=json.loads(self.expectedResult.data)
        # )

      ret += "MockIncorrectResultException - Got call for " + str(self.recievedRequest) + " but data value mismatched"
      return ret
    return "MockIncorrectResultException - Got call for " + str(self.recievedRequest) + " but expected " + str(self.expectedResult)

class MockUnusedResultsException(Exception):
  unusedResults = None
  def __init__(self, unusedResults):
    self.unusedResults = unusedResults

  def __str__(self):
    return "There were " + str(len(self.unusedResults)) + " mock results not used"

class MockClass():
  stackOfExpectedReturnValues = None
  def __init__(self):
    self.stackOfExpectedReturnValues = []

  def registerNextResponse(
    self,
    reqFnName,
    url,
    data,
    #code,
    #error_type,
    status_code,
    contentBytes,
    contentHeaders=None,
    ignoreData=False
  ):
    the_response = Response()
    the_response.request = mockRequestClass(method=reqFnName, url=url)
    #the_response.code = code
    #the_response.error_type = error_type
    the_response.status_code = status_code
    if contentBytes is None:
      the_response._content = b""
    else:
      the_response._content = base64.b64decode(contentBytes)
    if contentHeaders != None:
      the_response.headers=contentHeaders
    self.stackOfExpectedReturnValues.append(
      ExpectedResult(
        reqFnName=reqFnName,
        url=url,
        data=data,
        response=the_response,
        ignoreData=ignoreData
      )
    )

  def returnNextResult(
    self,
    reqFnName,
    url,
    data
  ):
    recievedRequest = ExpectedResult(reqFnName, url, data)
    if (len(self.stackOfExpectedReturnValues)==0):
      raise MockNoResultSetupException(recievedRequest=recievedRequest)
    expectedResult = self.stackOfExpectedReturnValues.pop()
    if not expectedResult.requestMatches(reqFnName=reqFnName, url=url, data=data):
      raise MockIncorrectResultException(recievedRequest=recievedRequest, expectedResult=expectedResult, recievedData=data)
    return expectedResult.getResponse()

  def testComplete(self):
    if (len(self.stackOfExpectedReturnValues)!=0):
      print("Test complete but unused mock resutls - unwinding stack")
      origStack = copy.deepcopy(self.stackOfExpectedReturnValues)
      while (len(self.stackOfExpectedReturnValues) > 0):
        expectedResult = self.stackOfExpectedReturnValues.pop()
        print(expectedResult)

      raise MockUnusedResultsException(origStack)
