# Quick Start

This page aims to show a rough and ready quick tour of the libraries basic functionality.

All the following examples require that you run the following setup:

```
pip3 install EllucianEthosPythonClient
```

## Check library version

Run a python3 REPL console and type the following:

```
import EllucianEthosPythonClient
print(EllucianEthosPythonClient.__version__)
```
This should output the version of the library that is installed. (If this dosen't work check you ran the pip install command)

## Call an API to fetch a resource, change it and save back to Ethos

This sample will create a login session for the Ethos hub and use it to retrieve a resource:

Start a python3 REPL console and run the following to setup the varaibles required. In this example I am using the 
persons resource.
 
```
ethosBaseURL = "ETHOS BASE URL e.g. https://integrate.elluciancloud.ie no trailing slash"
ethosAPIKey = "ETHOS APPLICATION API KEY"
resourceName = "persons"
personResourceID = "A_PERSON_GuiD"
```
(Replace the values above with values from your environment)

Note: In a real APP ethosAPIKey will be read from some sort of secure store, and ethosBaseURL should be a configurable 
paramater

Now create client and login session objects:
```
import EllucianEthosPythonClient
ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)
```

Now you can call the API to get a resource:
```
person = ethosClient.getResource(
  loginSession=loginSession,
  resourceName=resourceName,
  resourceID=personResourceID,
  version=None
)
```
The version paramater is optional and if you want to retrieve a specific version you can supply a string such as "12.1.0"

If the resource is not found the getResource function will return None.
Otherwise it will return an Resource Wrapper Object. You can print the details of the object you returned as follows:

```
print("API version from response:", person.version)
print("GUID of returned resource=", person.resourceID)
print(person.dict)
```

Most getResource calls will return a result class of BaseResourceWrapper however if the resource name and version is 
recognised by the library the object returned will be a class designed for that object and version. This class may provide 
special operations for that resource type. You can find the class that was returned with the following:

```
print("Resource Type Object=", type(person).__name__)
```
                          
See [ResourceWrappers](/EllucianEthosPythonClient/ResourceWrappers/README.md) for information.

You can make a change to the resource by altering the dict structure. The following code adds a 2 to the end of the
persons last name then calls the api to save it back to Ethos:
```
print("Lastname is currently " + person.dict["names"][0]["lastName"])
person.dict["names"][0]["lastName"] = person.dict["names"][0]["lastName"] + "2"
person.save(loginSession=loginSession)
```

One thing to remember about this method is that the entire person record is saved back to Ethos. If an hour or two has
elapsed between fetching the resource and saving it then there is a danger that any other changes to the source record
will be overwritten. It's best to read a record then immediatadly write it back to minimise this risk.

## Get a list of resources

This library provides a python iterator which handles the pagination. The following example collects
resources 25 at a time using the iterator. (It stops after 123 so it won't run forever) 

You can run this in the REPL:
```
personHoldIterator = ethosClient.getResourceIterator(
  loginSession=loginSession,
  resourceName="person-holds",
  params=None,
  version=None,
  pageSize=25
)

max = 123
cur = 0
for personHold in personHoldIterator:
  print("personHold", personHold.dict["person"]["id"], personHold.dict["startOn"])
  cur += 1
  if cur > max:
    break
```

For more information on using resource iterators see [resource iterators](./RESOURCEITERATORS.md)

## Create a new resource

The following example creates a new person hold. This can be run in the REPL once the GUID's for person and 
person hold category are filled in:

```
personGUID="TO BE ENTERED"
personHoldCategoryGUID="TO BE ENTERED"

personHoldToCreate = {
    'endOn': '2099-12-31T00:00:00Z',
    'person': {'id': personGUID},
    'startOn': '2020-01-17T00:00:00Z',
    'type': {
      'category': 'academic',
      'detail': {
        'id': personHoldCategoryGUID
      }
    }
  }

createdPersonHold = ethosClient.createResource(
  loginSession=loginSession,
  resourceName="person-holds",
  resourceDict=personHoldToCreate,
  version="6"
)

print("Created a new person-hold resource with id ", createdPersonHold.version)
print("GUID of returned resource ", createdPersonHold.resourceID)

```

## Delete a resource

There are two ways to delete a resource. Firstly you can use the delete method from a returned resource.
The following examples delete the resource created in the previous example:
```
createdPersonHold.delete(loginSession=loginSession)
```

The disadvantage to this method is that you must first query the resource to obtain an object.
Another method to delete a resource requires just the resoruce guid:
```
recourceGUIDToBeDeleted = createdPersonHold.resourceID
ethosClient.deleteResource(
  loginSession=loginSession,
  resourceName="person-holds",
  resourceID=recourceGUIDToBeDeleted
)
```

## Call any other API

This library wraps a lot of API calls to make them easier to use in Python. Not every API call is wrapped in the library
and they may not be wrapped in the way that is reburied. You can still use the library to make these calls and handle
the security. See [direct call guide](DIRECTCALL.md) for examples.

## Next Steps

This quick start guide has stepped through most of the major features of the library.
The library has also an implementation of a poller which can be used to call the publish API and retrieve change 
notifications it is explained in more detail here - [Poller Guide](POLLERGUIDE.md).


