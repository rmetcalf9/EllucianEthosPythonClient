
from .ResPersons import registerKnownResourses as registerPersonsKnownResourses
from .BaseResourceWrapper import BaseResourceWrapper

knownResourses = {}
registerPersonsKnownResourses(knownResourses)

def getResourceWrapper(clientAPIInstance, dict, version, resourseName):
  if resourseName in knownResourses:
    if knownResourses[resourseName](version) is not None:
      return knownResourses[resourseName](version)(clientAPIInstance, dict, version, resourseName)
  return BaseResourceWrapper(clientAPIInstance, dict, version, resourseName)
