# dcbot-image-downloader
## Abstract
* You can run this bot on your conputer then invite it into your discord server
* It will automatically check message in specific channels then download and classify twitter and pixiv images
## How to use
### Install these python packages
```
discord
tweepy
requests
pixivpy3
urllib3
dotenv
```
### Setup .env
```
# path
IMAGE_FOLDER_PATH = ''
DICT_PATH = ''

# tweepy
TWEEPY_BEARER_TOKEN = ''
TWEEPY_CONSUMER_TOKEN = ''
TWEEPY_CONSUMER_SECRET = ''

# pixiv
REFRESH_TOKEN = ''

# dc bot
TOKEN = ''
CHANNEL_LIST = '[]'
USER_ID = 
```


| .env variable | Discription |
| -------- | -------- |
| IMAGE_FOLDER_PATH | The path you want to download images in |
| DICT_PATH | A hashtag-Directory dictionary to help this bot auto-classify|
|TWEEPY_BEARER_TOKEN| Get from [Twitter Developer](https://developer.twitter.com/en)|
|TWEEPY_CONSUMER_TOKEN| Get from [Twitter Developer](https://developer.twitter.com/en)|
|TWEEPY_CONSUMER_SECRET| Get from [Twitter Developer](https://developer.twitter.com/en)|
|REFRESH_TOKEN|Get from https://github.com/eggplants/get-pixivpy-token |
|TOKEN|Get from [Discord Developer](https://discord.com/developers/applications)|
|CHANNEL_LIST|The specific channel list you want to download image from|
|USER_ID|Your discord user id for this bot to send the state messages|

### Create a new application and add a bot in Discord Developer Portal
* Privileged Gateway Intents: "SERVER MEMBERS INTENT", "MESSAGE CONTENT INTENT"
![](https://i.imgur.com/R8r1e6o.png)


### Invite this dc bot into your server
* Developer portal -> application -> OAuth2 -> URL generator -> scope:bot
-> bot permissions: "Read Messages/View Channels", "Send Messages", "Attach Files"
 ![](https://i.imgur.com/uanZoRg.png)

Invite link will like this type:
https://discord.com/api/oauth2/authorize?client_id=xxxxxxxxxxx&permissions=35840&scope=bot
### Run this program
### Done!
