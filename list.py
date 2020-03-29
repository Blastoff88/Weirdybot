import os
import slack

token = os.environ["SLACK_TOKEN"]
client = slack.WebClient(token=token)

users = client.users_list() 
for u in users["members"]:
    # print(u["name"])
    if u["name"] == "joekutner":
        print(f'{u["name"]} id is {u["id"]}')