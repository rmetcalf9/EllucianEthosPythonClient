import sys
import os

# This sample uses a resource iterator to list all the academic periods

import EllucianEthosPythonClient

ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosAppAPIKey = os.environ["ICETHOSDEVAPIKEY"]


ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAppAPIKey)

print("Start")

def isYes(str):
  pro = userInput.strip().upper()
  if len(pro)<1:
    return False
  return pro[0]=="Y"

params = {}
userInput = input("Do you want to restrict to periods with open registration? (Y/N)")

if isYes(userInput):
  print("Restricting results where registration is open")
  params["criteria"] = "{\"registration\":\"open\"}"

academicPeriodIterator = ethosClient.getResourceIterator(
  loginSession=loginSession,
  resourceName="academic-periods",
  version=None,
  params=params,
  pageSize=25
)

cur = 0
for period in academicPeriodIterator:
  cur += 1
  print(cur, "period", period.dict)

print("End")
