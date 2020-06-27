# Calling Ethos API directly using API


This library wraps a lot of API calls to make them easier to use in Python. Not every API call is wrapped in the library
and they may not be wrapped in the way that is requried. There are functions that allow direct calls to the API:

- sendGetRequest
- sendPostRequest
- sendPutRequest
- sendDeleteRequest

Each takes a loginsession argument. If supplied the loginsession will add the authorization header to calls and handle
retrying 401 responses. If loginsession is passed as "None" then no headers are added.
 
You also need to supply an injectHeadersFn function. This function can be used to add what ever header is required to
the API call. See the examples for mode details.

The following examples show calling the API directly whilst still using the library to handle API security: 

## Example get Request

```
exampleURL = "/api/persons/SOMEPERSONGUID"
exampleVersion = "6"

def sampleInjectHeaderFunctionForGet(headers):
  headers["Accept"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"

result = ethosClient.sendGetRequest(
  url=exampleURL,
  loginSession=loginSession,
  injectHeadersFn=sampleInjectHeaderFunctionForGet
)

print(result.status_code)
print(result.content)

```

## Example Post Request

```
exampleURL = "/api/persons/SOMEPERSONGUID"

def sampleInjectHeaderFunctionForPost(headers):
    headers["Accept"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"
    headers["Content-Type"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"

postDict = { "TODO": "PutDataHere" }

result = ethosClient.sendPostRequest(
    url=exampleURL,
    loginSession=loginSession,
    injectHeadersFn=sampleInjectHeaderFunctionForPost,
    data=json.dumps(postDict)
)

print(result.status_code)
print(result.content)
```

## Example Put Request

```
exampleURL = "/api/persons/SOMEPERSONGUID"
exampleVersion = "6"

def sampleInjectHeaderFunctionForPut(headers):
  headers["Accept"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"
  headers["Content-Type"] = "application/vnd.hedtech.integration.v" + exampleVersion + "+json"

putDict = { "TODO": "PutDataHere" }

result = ethosClient.sendPutRequest(
  url=exampleURL,
  loginSession=loginSession,
  injectHeadersFn=sampleInjectHeaderFunctionForPut,
  data=json.dumps(putDict)
)

print(result.status_code)
print(result.content)

```

## Example Delete Request

For delete requests in Ethos no extra headers are required so the injectHEadersFn can be set to None.

```
exampleURL = "/api/persons/SOMEPERSONGUID"

result = ethosClient.sendDeleteRequest(
    url=exampleURL,
    loginSession=loginSession,
    injectHeadersFn=None
)

print(result.status_code)
print(result.content)

```

## Handling Responses

The return value of these functions is a standard python requests response object.

Note: With built in API calls the library will check the response code is correct and raise Exceptions. When you call
the API's with this method you are responsible for checking the response is correct and for converting the output to a 
python structure, an example for doing this is:

```
if result.status_code != 200:
    raise Exception("An API Error has occured")

resultDict = json.loads(result.content)

```
