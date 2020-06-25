# Poller Guide

This guide goes through how to use the poller implementation in the library which can be used to subscribe to change
notifications.

There are two ways of using the Poller

 1. Queue based method
 2. Function based method
 
 You can go through this guide using a python 3 REPL. This will demonstrate using the poller in both modes.
 
 # Setup

 ## Ethos Setup
 
 This guide should be only used against a development environment as it will change data in the Banner instance.
 
 To go through this guide you need a stream of messages to poll. This guide uses the person-holds resource type and the
 testing environment is setup to provide this.   
 
 Before starting in Ethos you should:
 
  - Create an application in the Ethos Integrations UI. Make sure the application is subscribed to the "person-holds" resource.
  - Created application needs the credentials setup so it can query person-holds resources
  - Get the APIkey for the application that is created
 
 ## Local developer machine setup
 
 Install the latest version of the library with the following command:
 ```
pip install EllucianEthosPythonClient
```
 
 The library contains a sample Python script which can be used to generate a stream of changes. It works by creating and
 then deleting person-holds messages for a supplied list of person guids. It only requires a single file from the
 repository to be placed on the developers machine so no need to clone the git repository.
 
  1. Make a local copy of [generateChanges.py](../samples/generateChanges.py) - this can be done by copying and pasting
  into a local file if required
  2. Change the line that assigns ethosBaseURL so that the URL is set on your system
  3. Change the line that assigns ethosAPIKey so it is set to the ethosAPIKey for the application that was created.
  4. Change the personResourceIDList so it contains a list of personGUIDS in the environment that is to be tested.
  5. Change the personHoldCategoryGUID to match an academic category hold on the environment.
 
 This process works by going through the personResourceIDList and creating a hold for each person. Once it has created 
 a hold for each person it then goes through and deletes the holds it has created. It does this continuously until ctrl+c
 is pressed at which point it deletes any remaining holds it has created and exits.
  
 If required you can inspect the personHOLD JSON that the sample will use to create and change more than the 
 personHoldCaretoryGUID.
 
 Run the sample on the developer machine with a command like:
```
python ./generateChanges.py
```

The program will output a + each time it creates a hold, and a - when it deletes one.
You can also use the Ethos UI to inspect the application that has been created. You should see the number of waiting
messages for the application start to incement.

You can keep this process running whilst following the rest of the steps in another window.

 # Queue based mode
 
 All the following commands should be typed into a python 3 REPL console.
 
import libraries we will use:
```
import EllucianEthosPythonClient
import queue
import os
```

Setup variables that contain baseurl and api key. In the example below I read these from the 
developer machines environment but this can be changed to constant values if required:
```
ethosBaseURL = os.environ["ETHOSBASEURL"]
ethosPollerAppAPIKey = os.environ["ETHOSPOLLERAPIKEY"]
```

Setup the API Client instance and create a login session:
```
ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosPollerAppAPIKey)
```

Now we will create a queue which will receive the messages read from Ethos. This is a standard python thread safe queue:
```
changeNotificationQueue = queue.Queue()
```

The following command will check the number of messages in our python queue:
```
print(changeNotificationQueue.qsize())
```

This will output zero as there is currently nothing in the python queue. To get messages into our queue we need to tell
the API client to start polling Ethos and retrieving messages:

```
ethosClient.startChangeNotificationPollerThread(
  loginSession=loginSession,
  frequency=10,  # number of seconds between fetches
  pageLimit=20,  # number of change notifications to get per requests
  maxRequests=4,  # maximum number of rquests to use in each fecth
  pollerQueue=changeNotificationQueue
)
```

Running this code causes the API client to launch a background thread. Every 10 seconds the thread will make API calls
to Ethos to fetch any change notifications and deliver them to the python queue. The maxRequests paramater controls how
many times the API client will keep asking Ethos for more messages and effectively puts an upper limit on the number of
messages that will be taken in a 10 second period. (In this case a maximum of 4*20=80 messages can be collected in 10
seconds) The best values to put here will differ depending on the usecase.

The thread runs in the background and may raise an exception without us knowing. If this happens we would like our
programs to raise an exception rather than ignore it. The following command will check the health of the thread and
re-raise any exceptions it has encountered. 
```
ethosClient.healthCheck()
```
(In a real program this will be called from the main loop)

If you leave the thread running for a while you should notice the number of waiting messages in Ethos 
start to decrease. You can then re-run the following command and see how many messages are waiting in the queue:
```
print(changeNotificationQueue.qsize())
```

You should now get a non-zero result!

This is a standard python queue so we can take the first message from the queue as follows:
```
changeNotificationRecieved = changeNotificationQueue.get()
print(changeNotificationRecieved)
```

The get function takes the next message from the queue.

Now changeNotificationRecieved is a ChangeNotificationMessage object and you can find more information about the change
as follows:
```
print("Operation:", changeNotificationRecieved.operation)
print("Published:", changeNotificationRecieved.published)
print("resourceName:", changeNotificationRecieved.resourceName)
print("resourceID:", changeNotificationRecieved.resourceID)
print("resourceWrapper:", changeNotificationRecieved.resourceWrapper)
```  

The value you receive for resourceWrapper will either be None or a resource object. If it is none this is because Ethos
will not send the resource content for delete operations. If you saw none in the command above you can keep taking
messages from the queue until you see an example which does not contain none.

Once you have a resourceWrapper you can use it in the same way you use objects returned from the getResource function:
```
print("API version:", changeNotificationRecieved.resourceWrapper.version)
print("GUID:", changeNotificationRecieved.resourceWrapper.resourceID)
print("Data:", changeNotificationRecieved.resourceWrapper.dict)
```

One thing to remember is that you never know how long messages have been hanging round in queues. If your aim is to 
update records you should avoid writing stale data by re-querying the resource to get an uptodate version.
This will reduce the chance of overwriting a change made by another process while the record was waiting in the queue.
The resource wrapper includes refresh function can do this automatically:

```
changeNotificationRecieved.resourceWrapper.refresh(loginSession=loginSession)
```

(In the test example person-holds are being created and deleted so the refresh may fail because the resource is already 
deleted)

This causes API client to update the resource data with new information from Ethos.

We wouldn't normally handle the messages one at a time in the REPL. Lets output everything we have in our queue:

```
while changeNotificationQueue.qsize()>0:
  changeNotification = changeNotificationQueue.get()
  print("Recieved", changeNotification.operation, changeNotification.resourceName, changeNotification.resourceID)
```

You should see everything that has been recieved in the queue.


Finally before we terminate we must remember we have started a background thread. It should be stopped as follows:
```
ethosClient.close()
```

See [simplePollerExample.py](../samples/simplePollerExample.py) for an example of a python program that uses this method
to process Ethos change notifications. This shows how you can continously process the messages in the python queue.

## Pros an cons of the queue based method

The queue based mode is decoupled and efficient. It does not require storing any high water marks locally.
This means you can launch mutiple instances of the python application to increase the throughput of the system.
However if your python program were to crash messages stored in it's
queue will be lost. This may be acceptable if you have some way other way of retransmitting the messages in the event of
failure.

 # Function based mode
 
 The ethos change notification process allows clients to persist the lastprocessedid into local storage. This is
 required to provide a reliable message subscription process. The disadvantage of this is that each single page of
 messages must be completly processed before the next page is requested.
 
 To use the poller in this mode you must provide a function which processes each message and persists the lastprocessedid
 to a file store.
 
 In the exmaples here we will use a file as my presistant store for lastprocessedid. I will create a string variable to
 hold the filename:
 
```
lastprocessid_FileName = "./pollerguideTempFileForLastProcessedID.txt"
```

Setup the file to contains just a 0.
```
with open(lastprocessid_FileName, 'w') as filetowrite:
    filetowrite.write('0')
```

Next we need to prepare a function for the library to call that will process each message.
The requiremnts for the function are:
 - accept three parameters apiClient, messageid, changeNotification
 - process the message and commit any transactions
 - write the messageid passed in as the lastprocessedid
 - return True if the message was processed sucessfully
 - return False or raise an exception otherwise
 
If the function returns False the poller will terminate. This causes it to stop reading messages from Ethos and when the
application is started again it can start from the last successfully recorded poller id.
 
```
def processSingleMessage(apiClient, messageid, changeNotification):
    # in a real example this part would write to file or update a db
    print("received msgid ", messageid, changeNotification.operation,  changeNotification.resourceName, changeNotification.resourceID)
    with open(lastprocessid_FileName, 'w') as filetowrite:
        filetowrite.write(messageid)
    return True
```

This exmaple just outputs to the screen. In a real example it would write to a file or db and commit the transaction.

The change notificaiton object is the same as the one that is retrieved from the queue in queue mode so all the same 
operations are available. 

You can only start the poller thread once so we will create a new ethosClient instance. (Hopefully you haven't forgotten
to stop the previous thread by calling ethosClient.close())

```
ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=ethosBaseURL)
loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=ethosPollerAppAPIKey)
```

In order to start the thread we will need to fetch the lastprocessid from the file:
```
lastProcessedID=""
with open(lastprocessid_FileName, 'r') as filetowrite:
    lastProcessedID=filetowrite.read()
```

Then just as before we start the poller thread but this via a different method which allows us to pass the function we 
defined before:

```
ethosClient.startChangeNotificationPollerThreadInFunctionMode(
  loginSession=loginSession,
  frequency=10,  # number of seconds between fetches
  pageLimit=20,  # number of change notifications to get per requests
  maxRequests=4,  # maximum number of rquests to use in each fecth
  lastProcessedID=lastProcessedID,
  messageProcessingFunction=processSingleMessage
)
``` 

You can still use the healthCheck function to raise any exceptions that occur in the thread:
```
ethosClient.healthCheck()
```

If the generateChanges function you started before is still running you should see the output appear on the screen.

When done the background thread still needs to be stopped: 
```
ethosClient.close()
```  

See [simpleFunctionModePollerExample.py](../samples/simpleFunctionModePollerExample.py) for an example of a python program that uses this method
to process Ethos change notifications.


 ## Pros an cons of the function based method

The advantage of the function based method is the use of the lastprocessedid to make sure messages are not lost.
This means that only a single instance of the application can be run and you must store the lastprocessed id in a
reliable storage location.
The speed of processing the messages is reduced as confirmation of transmission is requried before the process moves on
to the next message.
