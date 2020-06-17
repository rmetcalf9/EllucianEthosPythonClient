from .APIClients import LoginSession


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

  def _getNewAuthToken(self):
    self.currentAuthKey = None
    charset = "UTF-8"

    def injectHeaderFN(headers):
      headers["Accept-Charset"] = charset
      headers["Content-Type"] = "application/x-www-form-urlencoded" + ";charset=" + charset
      headers["Authorization"] = "Bearer " + self.apikey

    result = self.APIClient.sendPostRequest(
      url="/auth",
      data=[],
      loginSession=None,
      injectHeadersFn=injectHeaderFN
    )
    if result.status_code != 200:
      return None

    self.currentAuthKey = result.content.decode(charset)

  def injectHeaders(self, headers):
    headers["Authorization"] = "Bearer " + self.currentAuthKey

  def refresh(self):
    self._getNewAuthToken()
    if self.currentAuthKey is None:
      return False
    return True
