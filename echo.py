import os
from slack import RTMClient

@RTMClient.run_on(event="message")
def echo(**payload):
    data = payload['data']
    print(data["text"])

token = os.environ["SLACK_TOKEN"]
rtm_client = RTMClient(token=token)
rtm_client.start()