import os
import slack

token = os.environ["SLACK_TOKEN"]
client = slack.WebClient(token=token)

i = 1
while i < 2:
    client.chat_postMessage(
        channel="UGQHP14RK",
        text="<@UGQHP14RK> what is your favorite type of cheese?"
    )
    i = i + 1
    print(i)