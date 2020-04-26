import os
import slack
from dotenv import load_dotenv
load_dotenv(verbose=True)

token = os.environ["SLACK_TOKEN"]
client = slack.WebClient(token=token)

users = client.users_list() 
for u in users["members"]:
    if "real_name" in u:
        print(u['real_name'])
    # if u["name"] == "weirdybot":
    #     print(f'{u["name"]} id is {u["id"]}')

# channels = client.channels_list()
# for c in channels["channels"]:
#     print(c["name"] + " = " + c["id"])