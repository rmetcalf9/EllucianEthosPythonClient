#Quick Start

This page aims to show a rough and ready approach to checking the library is installed and working.

All the following examples require that you run the following setup:

```
pip3 install EllucianEthosPythonClient
```

## Check library version

Run a python3 console and type the following:

```
import EllucianEthosPythonClient
print(EllucianEthosPythonClient.__version__)
```
This should output the version of the library that is installed. (If this dosen't work check you ran the pip install command)

## Call an API to fetch a resource

this sample will create a login session for the Ethos hub and use it to retrieve a resource:

Start a python3 console and run the following to setup the varaibles required. 
```
ethosBaseURL = "ETHOS BASE URL e.g. https://integrate.elluciancloud.ie no trailing slash"
ethosAPIKey = "ETHOS APPLICATION API KEY"
resourceID = "A_PERSON_GuiD"
```
(Replace the values above with values from your environment)

Next create client and login session objects:
```
import EllucianEthosPythonClient
ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosAPIKey)
```

Now you can call the API to get a resource:
```
person = ethosClient.getResource(
  loginSession=loginSession,
  resourceName="persons",
  resourceID=personResourceID,
  version=6
)
```


TODO



