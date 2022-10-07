#導入 Discord.py
import discord
import tweepy
import requests
import os
from pixivpy3 import *
import urllib3
import json
import csv
from dotenv import load_dotenv
load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

image_folder_path = os.getenv("IMAGE_FOLDER_PATH")
dict_path = os.getenv("DICT_PATH")

dd_dic = {}

def initial_dic():
	dd_dic.clear()
	with open(dict_path, newline='',encoding='utf-8-sig') as csvfile:
		rows = csv.reader(csvfile)
		for row in rows:
			dd_dic[row[0]] = row[1]

def get_tweet_id(tweeter_url):
    id_start = tweeter_url.rfind("/status/")
    id_end = tweeter_url.rfind("?")
    id_end2 = tweeter_url.rfind("/photo/")
    if id_end == -1 or (id_end > id_end2 and id_end2 != -1):
        id_end = id_end2

    if id_end != -1:
        id = tweeter_url[id_start+8:id_end]
    else:
        id = tweeter_url[id_start+8:]
    return id


def download_image_from_twitter(tweeter_url,image_folder_path):
    try:
        client = tweepy.Client(bearer_token= os.getenv("TWEEPY_BEARER_TOKEN"),
                                consumer_key = os.getenv("TWEEPY_CONSUMER_TOKEN"),
                                consumer_secret = os.getenv("TWEEPY_CONSUMER_SECRET"))

        id = get_tweet_id(tweeter_url)

        tweets = client.get_tweets(ids=id,tweet_fields=['context_annotations', 'created_at'],
                                            media_fields=['url'], expansions='attachments.media_keys')

        # Get list of media from the includes object
        media = {m["media_key"]: m for m in tweets.includes['media']}
        hashtags = []

        for tweet in tweets.data:
            attachments = tweet.data['attachments']
            media_keys = attachments['media_keys']
            text = tweet.text.strip().replace(u'\u3000', u' ').replace(u'\xa0', u' ')
            hashtags = text.split('\n')

        ### 圖片下載的目標資料夾 ###
        dd_dir = []

        ### 從推特內文擷取hashtag ###
        for hashtag in hashtags:
            hashtag = hashtag.replace('＃','#')
            if hashtag.find('#') != -1:
                inline_hashtags = hashtag.split(' ')
                for inline_hashtag in inline_hashtags:
                    if inline_hashtag.find('#') != -1:
                        hashtag_units = inline_hashtag.split('#')
                        for hashtag_unit in hashtag_units:
                            tmp = dd_dic.get('#' + hashtag_unit)
                            if tmp != None:
                                dd_dir.append(tmp)
        #刪去重複hashtag
        dd_dir = list(set(dd_dir))

        ### 回傳給GUI的訊息 ###
        status_msg = ''

        ### 若hashtag沒有對應的人物或沒有hashtag，則下載至other ###
        if len(dd_dir) == 0:
            dd_dir.append('other')
            status_msg = f'{id} download to other: no hashtag info'

        ### 若多於一張圖片且hashtag多於一個，則下載至other ###
        elif len(media_keys) > 1 and len(dd_dir) > 1:
            dd_dir.clear()
            dd_dir.append('other')
            status_msg = f'{id} download to other: images have more than 1 hashtag'

        ### 若hashtag數過多，則下載至other ###
        elif len(dd_dir) > 5:
            dd_dir.clear()
            dd_dir.append('other')
            status_msg = f'{id} download to other: too many hashtags'
        
        image_folder_path += '/images/'

        ### 建立圖片的母資料夾 ###
        if not os.path.exists(image_folder_path):
            os.mkdir(image_folder_path)

        ### 根據連結下載圖片 ###
        for image_num,media_key in enumerate(media_keys):

            ### 取得圖片連結 ###
            input_image = media[media_key].url
            ### 將圖片轉成最大解析度 ###
            big_image = input_image[:-4] + "?format=jpg&name=4096x4096"

            ### 只有一張圖則將image_num設為-1，控制圖片名稱不附加編號
            if len(media_keys) == 1:
                image_num = -1

            for i in dd_dir:

                ### 建立角色的子資料夾 ###
                if not os.path.exists(image_folder_path + i):
                    os.mkdir(image_folder_path + i)
                    
                download_image(big_image,image_num, image_folder_path + i,image_id=id)

                image_path = f'{image_folder_path}{dd_dir[0]}/{id}'
                if image_num != -1:
                    image_path += '_0'
                image_path += '.jpg'

        ### 回應給GUI的訊息 ###
        if status_msg == '':
            status_msg = f'{id} is download to folder: ' + ', '.join(dd_dir)
        return status_msg, image_path
    except:
        status_msg = 'download failed'
        return status_msg, ''

def download_image_from_pixiv(url,image_folder_path):
    try:
        image_folder_path += '/images/'

        ### 建立圖片的母資料夾 ###
        if not os.path.exists(image_folder_path):
            os.mkdir(image_folder_path)
        
        image_folder_path += 'pixiv'
        ### 建立pixiv子資料夾 ###
        if not os.path.exists(image_folder_path):
            os.mkdir(image_folder_path)


        api = AppPixivAPI()
        api.auth(refresh_token=os.getenv("REFRESH_TOKEN"))

        headers = {'Referer': 'https://www.pixiv.net/'}
        image_id = int(url[url.rfind('/artworks/')+10:])

        json_result = api.illust_detail(image_id)
        illust = json_result.illust

        image_urls = []
        if illust.page_count > 1:
            for i in illust.meta_pages:
                image_urls.append(i['image_urls']['original'])
        elif illust.page_count == 1:
            image_urls.append(illust.meta_single_page['original_image_url'])

        ### 下載圖片 ###
        for image_num,image_url in enumerate(image_urls):
            ### 只有一張圖則將image_num設為-1，控制圖片名稱不附加編號
            if len(image_urls) == 1:
                image_num = -1
            download_image(image_url,image_num,image_folder_path,headers=headers,verify=False,image_id=image_id)
        
        image_path = f'{image_folder_path}/{image_id}'
        #傳給使用者第一張圖
        if image_num != -1:
            image_path += '_0'
        image_path += '.jpg'
              
        status_msg = f'{image_id} download to folder: pixiv'
        return status_msg, image_path
    except:
        status_msg = f'{image_id} download failed'
        return status_msg, image_path

def download_image(img_download_url,image_num,image_folder_path,headers='',verify='',image_id=''):

    ### 下載圖片, header跟verify是pixiv要用的 ###
    if headers == '' or verify == '':
        img = requests.get(img_download_url)
    else:
        img = requests.get(img_download_url,headers=headers,verify=verify)

    if image_num == -1:
        ### 開啟資料夾及使用ID命名圖片檔並寫入圖片的二進位碼，只有一張圖因此不加編號
        with open(f"{image_folder_path}/{image_id}.jpg", "wb") as file:  
            file.write(img.content)
    else:
        ### 開啟資料夾及使用ID命名圖片檔並寫入圖片的二進位碼，並且幫圖加上編號
        with open(f"{image_folder_path}/{image_id}_{image_num}.jpg", "wb") as file:  
            file.write(img.content)

class aclient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents = intents)
    
    async def on_ready(self):
        await self.wait_until_ready()
        print(f'we have logged in as {self.user}.')
        initial_dic()
client = aclient()

@client.event
#當有訊息時
async def on_message(message):
    
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return

    ### 若包含twitter.com或pixiv.net/artworks則嘗試下載並傳送訊息給使用者 ###
    ### 指定要讀取訊息的頻道，若channel_list為空則預設讀取所有頻道 ###
    channel_list = json.loads(os.getenv("CHANNEL_LIST"))
    if (message.channel.id in channel_list or len(channel_list) == 0) and ('twitter.com' in message.content or 'pixiv.net/artworks' in message.content):
        
        if 'twitter.com' in message.content:
            status, image_path = download_image_from_twitter(message.content,image_folder_path)
        elif 'pixiv.net/artworks' in message.content:
            status, image_path = download_image_from_pixiv(message.content,image_folder_path)
        
        user = await client.fetch_user(os.getenv("USER_ID"))
        await user.send(status)
        ### 傳送剛下載的檔案 ###
        if image_path != '':
            file = discord.File(image_path)
            await user.send(file = file)
        

client.run(os.getenv("TOKEN"))

