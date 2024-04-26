
# gp-discord-python
![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*gp-discord-python* is an API wrapper for Discord, written in Python.  
This library uses Oauth2 for authentication.
## Installing
```
pip install gp-discord-python
```
### Usage
```python
from discord.client import Client
client = Client("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")
client.set_bot_token("YOUR_BOT_TOKEN")
```
To obtain and set an access token, follow this instructions:
1. **Get authorization URL**
```python
url = client.authorization_url(redirect_uri="YOUR_REDIRECT_URI")
# This call generates the url necessary to display the pop-up window to perform oauth authentication
# param redirect_uri is required oauth request.
```
2. **Get access token using code**
```python
token = client.exchange_code("YOUR_CODE")
# "code" is the same response code after login with oauth with the above url.
```

3. **Refresh access token using refresh_token**
```python
token = client.refresh_token("YOUR_REFRESH_TOKEN")
# "refresh_token" is the token refresh in response after login with oauth with the above url.
```

## Actions

#### - Get user info
```python
client.get_user_info()
# Get the info for current user.
```
#### - Get by URL
```python
client.get_by_url(url="YOUR_URL")
# Get data for any other URL from Discord API.
```
#### - List of channels
```python
client.get_channel_list(guild_id="YOUR_GUILD_ID")
# Get data list for all channels in server account connected
# param guild_id is in the response of access token after exchange code authorization.
```
#### - Get messages
```python
client.get_messages(channel_id="YOUR_CHANNEL_ID")
# Get data list for all messages in a channel from server account connected
# param channel_id is in the response of list of channels action's.
```

#### - Send message

```python
import json

client.send_messages(
    channel_id="YOUR_CHANNEL_ID", 
    data=json.dumps({"content": "YOUR_MESSAGE_HERE"})
)
# Send message to channel from server account connected
# param channel_id is in the response of list of channels action's.
# param data is the content of message in format json
```
