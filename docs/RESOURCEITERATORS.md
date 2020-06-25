# Using Ethos Resource Iterators

The library has features which automatically handle the standard pagination process. It does this by generating resource
iterators that can be used just like python list structures.

## Simple iterator

The following sample will list all the academic periods.

```
academicPeriodIterator = ethosClient.getResourceIterator(
  loginSession=loginSession,
  resourceName="academic-periods",
  version=None,
  params=None,
  pageSize=25
)

cur = 0
for period in academicPeriodIterator:
  cur += 1
  print(cur, "period", period.dict)
```

In this example the iterator will collect periods 25 at a time, it then produces each academic period individually and
once 25 have been used up it will request the next page.

## Iterator with Parameters

There are various ways that Ethos API's accept criteria for selecting individual records.
e.g. for academic-periods this is documented [here](https://resources.elluciancloud.com/bundle/academic-periods/page/16.1.0/index.html)

The library caters for this by allowing you to send a dictionary of query paramaters which are added to the query 
requests. So for academic periods we can restrict to just listing open preiods:

```
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
```

You should refer to the Ethos documentation for the valid parameters that can be set for each resrouce type.

## Iterators from Resource Wrapper Objects

The libarary will recognise particular resource types and return custom resource weapper objects. If a custom resource
wrapper object is returned it may contain functions which return iterators for other related recources.

One example of this is getting a all visas for a person:
```
person = ethosClient.getResource(
  loginSession=loginSession,
  resourceName="persons",
  resourceID=personResourceID,
  version=None
)
print("Found:", person.dict["names"][0]["fullName"])

cur = 0
for curVisa in person.getVisas(loginSession=loginSession):
  cur += 1
  print(cur, "visa", curVisa.dict)
```

## Samples

 - Example program that lists academic periods - [listAcademicPeriods.py](../samples/listAcademicPeriods.py)
 - Example program that lists a persons addresses - [listPersonAddresses.py](../samples/listPersonVisas.py)