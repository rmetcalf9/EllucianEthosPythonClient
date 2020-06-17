from .APIClients import APIClientBase
from .EthosLoginSession import EthosLoginSessionBasedOnAPIKey

class EllucianEthosAPIClient(APIClientBase):
  refreshAuthTokenIfRequired = None

  def __init__(self, baseURL, mock=None):
    super().__init__(baseURL=baseURL, mock=mock)

  def getLoginSessionFromAPIKey(self, apiKey):
    return EthosLoginSessionBasedOnAPIKey(APIClient=self, apikey=apiKey)

  def getResource(self, loginSession, resourceName, resourceID, version=None):
    raise Exception("NI")
