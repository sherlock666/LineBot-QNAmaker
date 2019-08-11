import requests
import re
import configparser
import os
import random
import pandas as pd
import runpy
#叫入並執行其他.py用
import urllib
import time
import tempfile
import json
from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from imgurpython import ImgurClient
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction, URITemplateAction,PostbackTemplateAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,VideoSendMessage, ImageSendMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,ImagemapSendMessage, BaseSize, URIImagemapAction,
    ImagemapArea, MessageImagemapAction,
    Video, ExternalLink
)

##### Function Import #####
from tools.weather import weather

##### Main #####

app = Flask(__name__)

### another way using config.ini
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static')





### this part is constant  don't change
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'

##### QNA 設定區 勿動 #####
@app.route("/qnamaker", methods=['POST'])
def get_answer(message_text):

    url = "https://chevadymeowbotqna.azurewebsites.net/qnamaker/knowledgebases/4535ecb8-21ee-42c6-90a4-5b2529a710c4/generateAnswer"
    
    response = requests.post(
        url,
        json.dumps({'question': message_text}),
        headers={'Content-Type': 'application/json',
                'Authorization': '9b2c32d0-31e2-469b-8ed8-4ad1c93ad90d'
        }
        )

    data = response.json()

    try:
        if "error" in data:
            return data["error"]["message"]
        else:    
            answer = data['answers'][0]['answer']
            return answer
    except Exception:
        return "Error occurs when finding answer"

    
##### 處理訊息 #####

@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.source.user_id:", event.source.user_id)
    print("event.message.text:", event.message.text)
    print("event.source.type:", event.source.type)
    msg = get_answer(event.message.text)
    if msg == "No good match found in KB." :
        if event.message.text == "開始玩" or event.message.text == "功能表":
            student_program="\n\n*****實習計畫*****\n新聞\n電影\n遊戲資訊\n看廢文\n圖片(施工中)"
            tc_program="\n\n*****提攜專區*****\n施工中"
            association_program="\n\n*****協會專區*****\n施工中"
            dt_program="\n\n*****DT專區*****\n施工中"
            campaign_program="\n\n*****Campaign專區*****\n施工中"
            other="\n\n*****其他功能*****\n天氣預報"

            SelfReplyOnly="\n\n*****私聊限定*****\n!本區功能無法於群組使用!\n!請點選本帳號的聊天以使用!\n施工中"
            
            content = ("請輸入功能指令:"+student_program+association_program+dt_program+campaign_program+SelfReplyOnly+other+"\n\n幫助")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
######## 客製功能區 ########       
        if event.message.text == "aaa" :
            content = "哈囉"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0

#### 天氣預報 ####
        if event.message.text == "!天氣預報":
            content = "請輸入欲查詢地點\n(目前限台灣本島+離島)\n\n使用方式如下(已設有防呆):\n!台北市\n!臺北市\n!台北\n!臺北\n!taipei"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0

        if event.message.text == "!台北市" or event.message.text == "!臺北市" or event.message.text == "!台北" or event.message.text == "!臺北" or event.message.text == "!taipei":
            content = weather(L=0)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!新北市" or event.message.text == "!新北" or event.message.text == "!new taipei":
            content = weather(L=1)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!桃園市" or event.message.text == "!taoyuan":
            content = weather(L=2)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!台中市" or event.message.text == "!臺中市" or event.message.text == "!台中" or event.message.text == "!臺中" or event.message.text == "!taichung":
            content = weather(L=3)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!台南市" or event.message.text == "!臺南市" or event.message.text == "!台南" or event.message.text == "!臺南" or event.message.text == "!tainan":
            content = weather(L=4)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!高雄市" or event.message.text == "!高雄" or event.message.text == "!kaohsiung":
            content = weather(L=5)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!基隆市" or event.message.text == "!基隆" or event.message.text == "!keelung":
            content = weather(L=6)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!新竹縣" or event.message.text == "!hsinchu county":
            content = weather(L=7)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!新竹市" or event.message.text == "!hsinchu city":
            content = weather(L=8)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!苗栗縣" or event.message.text == "!苗栗" or event.message.text == "!miaoli":
            content = weather(L=9)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!彰化縣" or event.message.text == "!彰化" or event.message.text == "!changhua":
            content = weather(L=10)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!南投縣" or event.message.text == "!南投" or event.message.text == "!nantou":
            content = weather(L=11)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!雲林縣" or event.message.text == "!雲林" or event.message.text == "!yunlin":
            content = weather(L=12)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!嘉義縣" or event.message.text == "!chiayi county":
            content = weather(L=13)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!嘉義市" or event.message.text == "!chiayi city":
            content = weather(L=14)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!屏東縣" or event.message.text == "!屏東" or event.message.text == "!pingtung":
            content = weather(L=15)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!宜蘭縣" or event.message.text == "!宜蘭" or event.message.text == "!ilan":
            content = weather(L=16)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!花蓮縣" or event.message.text == "!花蓮" or event.message.text == "!hualien":
            content = weather(L=17)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!臺東縣" or event.message.text == "!台東" or event.message.text == "!taitung":
            content = weather(L=18)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!澎湖縣" or event.message.text == "!澎湖" or event.message.text == "!penghu":
            content = weather(L=19)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!金門縣" or event.message.text == "!金門" or event.message.text == "!jinmen":
            content = weather(L=20)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0
        if event.message.text == "!連江縣" or event.message.text == "!連江" or event.message.text == "!lianjiang":
            content = weather(L=21)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            return 0

############### 領袖營Menu ###############

        if event.message.text == "領袖營":
            camp_menu_messages = ImagemapSendMessage(
                base_url='https://i.imgur.com/3FiyO5o.png',
                alt_text='領袖營攻略手冊',
                base_size=BaseSize(width=1040, height=1040),
                actions=[
                    #Left 1
                    MessageImagemapAction(
                        text='行囊準備',
                        area=ImagemapArea(
                            x=0, y=119, width=535, height=135
                        )
                    ),
                    #Right 1
                    MessageImagemapAction(
                        text='遠征行程',
                        area=ImagemapArea(
                            x=533, y=119, width=507, height=134
                        )
                    ),
                    #Left 2
                    MessageImagemapAction(
                        text='營地駐紮',
                        area=ImagemapArea(
                            x=0, y=252, width=535, height=145
                        )
                    ),
                    #Right 2
                    MessageImagemapAction(
                        text='夥伴相認',
                        area=ImagemapArea(
                            x=534, y=251, width=506, height=146
                        )
                    ),
                    #Left 3
                    MessageImagemapAction(
                        text='戰區概況',
                        area=ImagemapArea(
                            x=0, y=395, width=535, height=135
                        )
                    ),
                    #Right 3
                    MessageImagemapAction(
                        text='RPG1',
                        area=ImagemapArea(
                            x=533, y=395, width=507, height=134
                        )
                    ),
                    #Left 4   
                    MessageImagemapAction(
                        text='RPG2',
                        area=ImagemapArea(
                            x=0, y=528, width=535, height=151
                        )
                    ),
                    #Right 4                                                          
                    MessageImagemapAction(
                        text='紙上談兵',
                        area=ImagemapArea(
                            x=533, y=528, width=505, height=151
                        )
                    )
                ]
            )
            line_bot_api.reply_message(event.reply_token,camp_menu_messages)
            return 0
########## 領袖營回覆 ##########
        if event.message.text == "行囊準備":
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/zBXhDLK.png',
                preview_image_url='https://i.imgur.com/zBXhDLK.png'
            )
            line_bot_api.reply_message(event.reply_token, image_message)
            return 0
        if event.message.text == "遠征行程":
            image_message_day_1 = ImageSendMessage(
                original_content_url='https://imgur.com/AC2ISii',
                preview_image_url='https://imgur.com/AC2ISii'
            )
            image_message_day_2 = ImageSendMessage(
                original_content_url='https://imgur.com/oVg1yiE',
                preview_image_url='https://imgur.com/oVg1yiE'
            )            
            line_bot_api.reply_message(event.reply_token, [image_message_day_1,image_message_day_2])
            return 0
        if event.message.text == "營地駐紮":
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/zBXhDLK.png',
                preview_image_url='https://i.imgur.com/zBXhDLK.png'
            )
            line_bot_api.reply_message(event.reply_token, image_message)
            return 0
        if event.message.text == "夥伴相認":
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/zBXhDLK.png',
                preview_image_url='https://i.imgur.com/zBXhDLK.png'
            )
            line_bot_api.reply_message(event.reply_token, image_message)
            return 0
        if event.message.text == "戰區概況":
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/zBXhDLK.png',
                preview_image_url='https://i.imgur.com/zBXhDLK.png'
            )
            line_bot_api.reply_message(event.reply_token, image_message)
            return 0
        if event.message.text == "RPG1":
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/zBXhDLK.png',
                preview_image_url='https://i.imgur.com/zBXhDLK.png'
            )
            line_bot_api.reply_message(event.reply_token, image_message)
            return 0
        if event.message.text == "RPG2":
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/zBXhDLK.png',
                preview_image_url='https://i.imgur.com/zBXhDLK.png'
            )
            line_bot_api.reply_message(event.reply_token, image_message)
            return 0
        if event.message.text == "紙上談兵":
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/zBXhDLK.png',
                preview_image_url='https://i.imgur.com/zBXhDLK.png'
            )
            line_bot_api.reply_message(event.reply_token, image_message)
            return 0






###############  ###############

######## 客製功能區 ########                
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
        return 0


if __name__ == '__main__':
    app.run()
