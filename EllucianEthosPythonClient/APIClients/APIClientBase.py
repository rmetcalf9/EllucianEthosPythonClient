import requests
from .Mock import MockClass

class APIClientException(Exception):
  result = None
  def __init__(self, result):
    self.result = result
  def getDescriptionString(self):
    ret = ""
    ret += "Failed API request\n"
    ret += "Request: " + str(self.result.request.method) + ":" + str(self.result.request.url) + "\n"
    ret += "Response: " + str(self.result.status_code) + ":" + self.result.content.decode() + "\n"
    return ret
  def __str__(self):
    return self.getDescriptionString()

class APIClientNotFoundException(APIClientException):
  def __init__(self, result):
    super(APIClientNotFoundException, self).__init__(result)



class APIClientBase():
  mock = None
  baseURL = None

  def __init__(self, baseURL, mock=None):
    if baseURL.endswith("/"):
      raise Exception("baseURL should not contain trailing slash: " + baseURL)

    if mock is None:
      self.mock = MockClass()
    else:
      self.mock = mock

    self.baseURL = baseURL

  def raiseResponseException(self, result):
    if (result.status_code == 404):
      raise APIClientNotFoundException(result)
    raise APIClientException(result)

  def sendRequest(self, reqFn, url, loginSession, data, origin, injectHeadersFn, refreshAttempted=False):
    if self.baseURL == "MOCK":
      return self.mock.returnNextResult(reqFnName=reqFn.__name__, url=url, data=data)

    # url must start with slash
    headers = {}
    if loginSession is not None:
      loginSession.injectHeaders(headers)
    if origin is not None:
      headers["origin"] = origin
    if injectHeadersFn is not None:
      injectHeadersFn(headers)

    print("headers", headers)

    result = reqFn(
      url=self.baseURL + url,
      data=data,
      headers=headers
    )
    if result.status_code == 401:
      if refreshAttempted:
        self.raiseResponseException(result)

      if loginSession.refresh(): #Returns true if loginSession refresh succeeded
        self.sendRequest(
          reqFn=reqFn,
          url=url,
          loginSession=loginSession,
          data=data,
          origin=origin,
          injectHeadersFn=injectHeadersFn,
          refreshAttempted=True
        )
      else:
        self.raiseResponseException(result)

    return result

  def sendGetRequest(self, url, loginSession, origin=None, injectHeadersFn=None):
    return self.sendRequest(reqFn=requests.get, url=url, loginSession=loginSession, data=None, origin=origin, injectHeadersFn=injectHeadersFn)

  def sendPostRequest(self, url, loginSession, data, origin=None, injectHeadersFn=None):
    return self.sendRequest(reqFn=requests.post, url=url, loginSession=loginSession, data=data, origin=origin, injectHeadersFn=injectHeadersFn)

  def sendDeleteRequest(self, url, loginSession, data=None, origin=None, injectHeadersFn=None):
    return self.sendRequest(reqFn=requests.delete, url=url, loginSession=loginSession, data=data, origin=origin, injectHeadersFn=injectHeadersFn)
