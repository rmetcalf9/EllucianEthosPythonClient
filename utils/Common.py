# Common functions used in utils
import os

def GetFromEnvironment(environVariable):
  if environVariable in os.environ:
    return os.environ[environVariable]
  raise Exception("Could not find " + environVariable + " in envionment for testing")



