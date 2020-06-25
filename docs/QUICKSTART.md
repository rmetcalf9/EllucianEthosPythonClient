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
resourceID = "A_PERSON_GuiD"
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
and they may not be wrapped in the way that is requried. The following example shows calling the API directly whilst
still using the library to handle API security: 

```
exampleURL = "/api/persons/SOMEPERSONGUID"
exampleVersion = "6"

def sampleInjectHeaderFunctionForGet(headers):
  headers["Accept"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"

result = self.sendGetRequest(
  url=exampleURL,
  loginSession=loginSession,
  injectHeadersFn=sampleInjectHeaderFunctionForGet
)

def sampleInjectHeaderFunctionForPost(headers):
    headers["Accept"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"
    headers["Content-Type"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"

postDict = { "TODO": "PutDataHere" }

result = self.sendPostRequest(
    url=exampleURL,
    loginSession=loginSession,
    injectHeadersFn=sampleInjectHeaderFunctionForPost,
    data=json.dumps(postDict)
)

def sampleInjectHeaderFunctionForPut(headers):
  headers["Accept"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"
  headers["Content-Type"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"

putDict = { "TODO": "PutDataHere" }

result = self.clientAPIInstance.sendPutRequest(
  url=exampleURL,
  loginSession=loginSession,
  injectHeadersFn=sampleInjectHeaderFunctionForPut,
  data=json.dumps(putDict)
)


result = ethosClient.sendDeleteRequest(
    url=exampleURL,
    loginSession=loginSession,
    injectHeadersFn=None
)

```

The return value of these functions is a standard python requests response object.

Note: With built in API calls the library will check the response code is correct and raise Exceptions. When you call
the API's with this method you are responsible for checking the response is correct and for converting the output to a 
python structure, an example for doing this is:

```
if result.status_code != 200:
    raise Exception("An API Error has occured")

resultDict = json.loads(result.content)

```

## Next Steps

This quick start guide has stepped through most of the major features of the library.
The library has also an implementation of a poller which can be used to call the publish API and retrieve change 
notifications it is explained in more detail here - [Poller Guide](POLLERGUIDE.md).


