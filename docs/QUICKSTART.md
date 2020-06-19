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
The version paramater is optional and if you want to retrieve a specific option you can supply a string such as "12.1.0"

If the resource is not found the getResource function will return None.
Otherwise it will return an Resource Wrapper Object. You can print the details of the object you returned as follows:

```
print("API version from response:", person.version)
print("GUID of returned resource=", person.resourceID)
print(person.dict)
```

Most getResource calls will return a result class of BaseResourceWrapper however if the resource name and version is 
recognised by the library the object returned will be a class designed for that object and version. This class may provide 
spacial operations for that resource type. You can find the class that was returned with the following:

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
)
```

One thing to remember about this method is that the entire person record is saved back to Ethos. If an hour or two has
elapsed between fetching the resource and saving it then there is a danger that any other changes to the source record
will be overwritten. It's best to read a record then immediatadly write it back to minimise this.

## Create a new resource

TODO

## Delete a resource

TODO

## Query back resources

TODO

## Call any other API

This library wraps a lot of API calls to make them easier to use in Python. Not every API call is wrapped in the library
and they may not be wrapped in the way that is requried. The following example shows calling the API directly whilst
still using the library to handle API security: 

TODO

The return value of these functions is a standard python requests response object.

Note: With built in API calls the library will check the response code is correct and raise Exceptions. When you call
the API's with this method you are responsible for checking the response is correct and for converting the output to a 
python structure, an example for doing this is:

```
if result.status_code != 200:
    raise Exception("An API Error has occured")

resultDict = json.loads(result.content)

```


