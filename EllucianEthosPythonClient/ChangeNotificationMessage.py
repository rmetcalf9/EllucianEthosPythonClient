from dateutil.parser import parse
import pytz
from .ResourceWrappers import getResourceWrapper

class ChangeNotificationMessage():
  clientAPIInstance = None
  messageID = None
  published = None
  operation = None
  resourceName = None
  resourceID = None
  resourceVersion = None
  resourceWrapper = None

  origDict = None

  def __init__(self, dict, clientAPIInstance):
    self.origDict = dict
    self.clientAPIInstance = clientAPIInstance
    self.messageID = dict["id"]

    dt = parse(dict["published"])
    self.published = dt.astimezone(pytz.utc)
    #print("rec:", dict["published"])
    #print("obj:", self.published)
    #print("out:", self.published.isoformat())

    self.operation = dict["operation"] #created, deleted, etc

    #These fields are always present - even for deleted operation
    self.resourceName = dict["resource"]["name"]
    self.resourceID = dict["resource"]["id"]
    if "version" in dict["resource"]:
      #version not sent for deleted operation
      self.resourceVersion = clientAPIInstance.getVersionIntFromHeader(dict["resource"]["version"])

    # for operation=deleted, the contentType is sent as empty
    # for operation=created, the content type is sent as resource-representation
    if dict["contentType"] == "resource-representation":
      self.resourceWrapper = getResourceWrapper(
        clientAPIInstance=self.clientAPIInstance,
        dict=dict["content"],
        version=self.resourceVersion,
        resourseName=self.resourceName
      )
    else:
      self.resourceWrapper=None

    #print("dict", dict)

    #Example message
    #{'id': '105',
    # 'published': '2020-06-23 09:26:24.732506+00',
    # 'resource': {
    #     'name': 'person-holds',
    #     'id': '7620b51d-acee-44cf-a4f9-85cc16f5c737',
    #     'version': 'application/vnd.hedtech.integration.v6+json'
    # },
    # 'operation': 'created',
    # 'contentType': 'resource-representation',
    # 'content': {
    #     'endOn': '2099-12-31T00:00:00Z',
    #     'id': '7620b51d-acee-44cf-a4f9-85cc16f5c737',
    #     'person': {'id': 'f1d31dd9-b141-4932-a8b6-d09637f1876d'},
    #     'startOn': '2020-01-17T00:00:00Z',
    #     'type': {
    #         'category': 'academic',
    #         'detail': {
    #             'id': '45182c89-6bb8-4996-a05a-6fce28f028eb'
    #         }
    #     }
    # },
    # 'publisher': {
    #     'id': '84592449-455b-40ea-9856-cb9e6878bd21',
    #     'applicationName': 'Imperial Student API - BILD'
    # }
    #}

  def getSimpleDict(self):
    return self.origDict