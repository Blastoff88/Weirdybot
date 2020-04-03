from slackeventsapi import SlackEventAdapter
import slack
import os
import random
import re
from dotenv import load_dotenv
load_dotenv(verbose=True)

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
token = os.environ["SLACK_TOKEN"]
slack_client = slack.WebClient(token=token)

weirdybot = "UU3N964UB"
channels = [
    "CUF9LSFTP", #bots
    "CGPDL914Y"  #1-random
]

def define_word(word, user, channel):
    message = "<@%s> The word %s is one very weird word. Here's a link to its definition: https://www.dictionary.com/browse/%s" % (user, word, word)
    slack_client.chat_postMessage(channel=channel, text=message)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    id = event_data["event_id"]
    message = event_data["event"]
    channel = message["channel"]
    if not channel in channels:
        print("ignoring message in channel: %s" % channel)
        return
    text = message.get("text") if "text" in message else ""
    user = message["user"] if "user" in message else ""
    print("message: id = " + id + ", text = " +text + ", channel = " +channel)    
    # If the incoming message contains "hi", then respond with a "Hello" message
    if weirdybot in user or weirdybot in text:
        print("it me!")
    elif message.get("subtype") is None and "robot" in text.lower():
        message = "Is someone talking about me? :robot_face:"
        slack_client.chat_postMessage(channel=channel, text=message)

# Example responder to greetings
@slack_events_adapter.on("app_mention")
def handle_mention(event_data):
    id = event_data["event_id"]
    time = event_data["event_time"]
    message = event_data["event"]
    user = message["user"]
    text = message.get("text")
    channel = message["channel"]
    if not channel in channels:
        print("ignoring message in channel: %s" % channel)
        return
    print("app_mention: id = " + id + ", text = " + text)
    # If the incoming message contains "hi", then respond with a "Hello" message
    if "favorite color?" in text.lower():
        colors = ["Blue",'Red',"Green","Brown","Fuchsia","Bleu cheese","Baby blue","Maroon","Lavender","Gray","Metal","Black. Oh yeah; that's not a color.","Beige","Tan",]
        message = "<@%s> %s" % (user, random.choice(colors))
        slack_client.chat_postMessage(channel=channel, text=message)
    elif "lego part" in text.lower():
        matches = re.findall("lego part [0-9]+", text.lower())
        if not matches:
            message = "<@%s> You did not post a part number. Please try again." % user
            slack_client.chat_postMessage(channel=channel, text=message)
        else:
            part = re.sub("lego part ", "", matches[0].lower())
            message = "<@%s> Here is a link to that part: https://brickset.com/parts/%s/" % (user, part)
            slack_client.chat_postMessage(channel=channel, text=message)
    elif "who are you" in text.lower():
        message = "<@%s> I am a robot. This is my source code: https://github.com/jkutner/Weirdybot" % user
        slack_client.chat_postMessage(channel=channel, text=message)
    elif re.findall("definition of the word [a-z]+", text.lower()):
        matches = re.findall("definition of the word [a-z]+", text.lower())
        word = matches[0].replace("definition of the word ", "")
        define_word(word, user, channel)
    elif re.findall("definition of [a-z]+", text.lower()):
        matches = re.findall("definition of [a-z]+", text.lower())
        word = matches[0].replace("definition of ", "")
        define_word(word, user, channel)
    elif re.findall("define the word [a-z]+", text.lower()):
        matches = re.findall("define the word [a-z]+", text.lower())
        word = matches[0].replace("define the word ", "")
        define_word(word, user, channel)
    elif re.findall("define [a-z]+", text.lower()):
        matches = re.findall("define [a-z]+", text.lower())
        word = matches[0].replace("define ", "")
        define_word(word, user, channel) 
    elif re.findall("meaning of the word [a-z]+", text.lower()):
        matches = re.findall("meaning of the word[a-z]+", text.lower())
        word = matches[0].replace("meaning of the word ", "")
        define_word(word, user, channel)
    elif re.findall("meaning of [a-z]+", text.lower()):
        matches = re.findall("meaning of [a-z]+", text.lower())
        word = matches[0].replace("meaning of ", "")
        define_word(word, user, channel)
    elif re.findall("[a-z]+ mean", text.lower()):
        matches = re.findall("[a-z]+ mean", text.lower())
        word = matches[0].replace("mean", "")
        define_word(word, user, channel)
    elif re.findall("[a-z]{8}", text.lower()):
        matches = re.findall("[a-z]{8}[a-z]*", text.lower())
        define_word(matches[0], user, channel)
    elif "hi" in text.lower():
        message = "Hello <@%s>! :weirdy:" % user
        slack_client.chat_postMessage(channel=channel, text=message)
    else:
        message = "<@%s> I'm not smart enough to understand that yet." % user
        slack_client.chat_postMessage(channel=channel, text=message)

# Example reaction emoji echo
# @slack_events_adapter.on("reaction_added")
# def reaction_added(event_data):
#     event = event_data["event"]
#     emoji = event["reaction"]
#     channel = event["item"]["channel"]
#     text = ":%s:" % emoji
#     slack_client.api_call("chat.postMessage", channel=channel, text=text)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
PORT = os.environ["PORT"]
slack_events_adapter.start(host="0.0.0.0", port=PORT)
