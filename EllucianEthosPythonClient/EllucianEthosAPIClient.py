from .APIClients import APIClientBase
from .EthosLoginSession import EthosLoginSessionBasedOnAPIKey

class EllucianEthosAPIClient(APIClientBase):
  refreshAuthTokenIfRequired = None

  def __init__(self, baseURL, mock=None):
    super().__init__(baseURL=baseURL, mock=mock)

  def getLoginSessionFromAPIKey(self, apiKey):
    return EthosLoginSessionBasedOnAPIKey(APIClient=self, apikey=apiKey)

  #Doc list https://xedocs.ellucian.com/xe-banner-api/ethos_apis/foundation/persons/person_get_guid_v6.html
  def getResource(self, loginSession, resourceName, resourceID, version=None):
    def injectHeaderFN(headers):
      if version is not None:
        headers["Accept"] = "application/vnd.hedtech.integration.v" + str(version) + "+json"

    result = self.sendGetRequest(
      url="/api/" + resourceName + "/" + resourceID,
      loginSession=loginSession,
      injectHeadersFn=injectHeaderFN
    )
    if result.status_code != 200:
      self.raiseResponseException(result)


    raise Exception("NI")

