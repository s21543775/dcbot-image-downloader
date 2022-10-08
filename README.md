# Dcbot Image Downloader
## Abstract
* You can run this bot on your conputer then invite it into your discord servers.
* It will automatically check message in specific channels then download and classify twitter and pixiv images.
* It names the image by tweet ID or pixiv image ID, so it can prevent user from downloading the same image.
* It will send the download info message directly to you, and won't generate any messages in discord servers.
![](https://i.imgur.com/uaD2Hdf.png)

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
 * You can set `DICT_PATH = './test_dic.csv'` for testing, this csv file contents are mostly about hololive and other vtubers' hashtag.
 * If you didn't set `CHANNEL_LIST`, that it defaults to read all channel in the server.
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
* Just double click it, .pyw will execute without showing the terminal window.
* Of course you can change it to .py or use terminal to execute it to debug.
### Done!
* You can send a tweet link which has images to check if it works.
![](https://i.imgur.com/gmfjB4W.png)
* if download successfully, this bot will send a message to you and tell you which directory this image downloads to.
* **it won't send any message to server, just sliently download images**

![](https://i.imgur.com/Uda9ohr.png)

