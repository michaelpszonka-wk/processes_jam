import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.DEBUG)

'''Very basic script taking in the Workiva POC slack app to send a notification to a channel
    Environment Variables: 
    SLACK_API_TOKEN - The slack app oauth token
    CHANNEL - The channel to send the notification to (note Workiva POC must already be invited to the channel)
    MESSAGE_CONTENT - The content within the message.  To @mention someone, format the username as <@userId>
'''

slack_token = os.getenv('SLACK_API_TOKEN')
channel = os.getenv('CHANNEL')
message_content = os.getenv('MESSAGE_CONTENT')

client = WebClient(token=slack_token)

try:
    response = client.chat_postMessage(
        channel=channel,
        text=message_content,
    )
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'