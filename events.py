from slackeventsapi import SlackEventAdapter
import slack
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
token = os.environ["SLACK_TOKEN"]
slack_client = slack.WebClient(token=token)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    id = event_data["event_id"]
    message = event_data["event"]
    print("message: id = " + id + ", text = " + message.get("text"))    
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message["user"] is "UU3N964UB" or "UU3N964UB" in message.get("text"):
        print("it me!")
    elif message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        slack_client.chat_postMessage(channel=channel, text=message)

# Example responder to greetings
@slack_events_adapter.on("app_mention")
def handle_mention(event_data):
    id = event_data["event_id"]
    time = event_data["event_time"]
    message = event_data["event"]
    print("app_mention: id = " + id + ", text = " + message.get("text"))
    # If the incoming message contains "hi", then respond with a "Hello" message
    if "hi" in message.get("text"):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        slack_client.chat_postMessage(channel=channel, text=message)
    else:
        channel = message["channel"]
        message = "I'm not smart enough to understand that yet."
        slack_client.chat_postMessage(channel=channel, text=message)

# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    slack_client.api_call("chat.postMessage", channel=channel, text=text)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
PORT = os.environ["PORT"]
slack_events_adapter.start(host="0.0.0.0", port=PORT)
