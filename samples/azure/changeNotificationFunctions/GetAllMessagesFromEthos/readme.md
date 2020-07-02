# TimerTrigger function designed to run every 5 minutes

This function runs every 5 minutes. It gets all the pending messages in the Ethos queue and adds them to an Azure queue
store 

## Application Settings

| Setting  | Description |
| ------------- | ------------- |
| AzureStorageQueuesConnectionString  | Get this from the access keys setting of the Azure Storage account |
| ethosBaseURL | Base url for accessing Ethos API e.g. X |
| ethosAppAPIKey | API key for Ethos application |


## Release command

```
func azure functionapp publish getEventsFromEthos
```