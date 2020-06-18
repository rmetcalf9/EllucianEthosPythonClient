
from .ResPersons import registerKnownResourses as registerPersonsKnownResourses
from .BaseResourceWrapper import BaseResourceWrapper

knownResourses = {}
registerPersonsKnownResourses(knownResourses)

def getResourceWrapper(clientAPIInstance, dict, version, resourseName):
  if resourseName in knownResourses:
    if version in knownResourses[resourseName]:
      return knownResourses[resourseName][version](clientAPIInstance, dict, version, resourseName)
  return BaseResourceWrapper(clientAPIInstance, dict, version, resourseName)
