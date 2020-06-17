from .APIClients import LoginSession


class EthosLoginSessionBasedOnAPIKey():
  APIClient = None
  apikey = None
  def __init__(self, APIClient, apikey):
    self.APIClient = APIClient
    self.apikey = apikey
