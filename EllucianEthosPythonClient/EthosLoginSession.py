from .APIClients import LoginSession
import requests

class EthosLoginSessionBasedOnAPIKey(LoginSession):
  APIClient = None
  apikey = None
  currentAuthKey = None
  def __init__(self, APIClient, apikey):
    self.APIClient = APIClient
    self.apikey = apikey

    self._getNewAuthToken()
    if self.currentAuthKey is None:
      raise Exception("Failed to establish login session using APIKey")

  def _getNewAuthToken(self, fromRefresh=False):
    self.currentAuthKey = None
    charset = "UTF-8"

    def injectHeaderFN(headers):
      headers["Accept-Charset"] = charset
      headers["Content-Type"] = "application/x-www-form-urlencoded" + ";charset=" + charset
      headers["Authorization"] = "Bearer " + self.apikey

    result = self.APIClient.sendRequest(
      reqFn=requests.post,
      origin=None,
      url="/auth",
      data=[],
      loginSession=None,
      injectHeadersFn=injectHeaderFN,
      skipLockCheck=fromRefresh
    )
    if result.status_code != 200:
      #print("_getNewAuthToken result got status code", result.status_code, " NOT 200")
      return None

    self.currentAuthKey = result.content.decode(charset)

  def injectHeaders(self, headers):
    headers["Authorization"] = "Bearer " + self.currentAuthKey

  def refresh(self):
    #print("Call to EthosLoginSession Refresh - getting new token")
    self._getNewAuthToken(fromRefresh=True)
    #print("get new auth token returned")
    if self.currentAuthKey is None:
      #print("no auth key so returning false")
      return False
    #print("Returning true to signal to retry origional request")
    return True
