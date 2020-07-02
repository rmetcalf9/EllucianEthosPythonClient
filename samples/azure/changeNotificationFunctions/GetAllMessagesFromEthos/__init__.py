import datetime
import logging
import json
import os

import azure.functions as func
import EllucianEthosPythonClient


def main(mytimer: func.TimerRequest, msg: func.Out[str]) -> None:

    ethosClient = EllucianEthosPythonClient.EllucianEthosAPIClient(baseURL=os.environ["ethosBaseURL"])
    loginSession = ethosClient.getLoginSessionFromAPIKey(apiKey=os.environ["ethosAppAPIKey"])

    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Requesting Change Notifications from Ethos at %s', utc_timestamp)

    outputDict = { "WouldHaveCalled": os.environ["ethosBaseURL"] }

    msg.set(json.dumps(outputDict))

