from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import json
import re

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    FlexSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    ButtonComponent,
    TextComponent,
    SeparatorComponent,
    BubbleContainer,
    BoxComponent,
    MessageAction
    )

import pyimgur

#function
from .dynamic_list_generator import favorite_list_generator #最愛清單function
from .datedo import datedo_list_generator  #對象工具列
from .carousel import carousel_list
from .report import draw

import numpy as np
import matplotlib.pyplot as plt   #問題所在


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
imgur_client=settings.IMGUR_CLIENT_ID

favorite_list=["小美","小花"] #最愛清單

attribute=[-0.1, 0.2, 0.3, 0.4, -0.3, 0.5] #各屬性分數

topic=["a","b","c"]#話題主題前三名

#主題1連結
topic1=["https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"]
#主題2連結
topic2=["https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"]
#主題3連結
topic3=["https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"]

@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)

        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        global favorite_list #全域變數
        global topic

        for event in events:

            if isinstance(event, MessageEvent):  # 如果有訊息事件

                if event.message.text == '最愛清單':
                    favorite_list_button=favorite_list_generator(favorite_list)
                    flex_message1=FlexSendMessage(alt_text='最愛清單',contents=favorite_list_button)
                    line_bot_api.reply_message(event.reply_token, flex_message1)

                elif re.match("搜尋對象:", event.message.text):
                    date=event.message.text[5:] # 對象名稱(date)
                    flex_message2=FlexSendMessage(alt_text=date,contents=datedo_list_generator(date))
                    line_bot_api.reply_message(event.reply_token, flex_message2)

                elif re.match("新增對象：", event.message.text):
                    favorite_list.append(event.message.text[5:])
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="成功新增對象:"+event.message.text[5:]))

                elif re.match("刪除對象:", event.message.text):
                    favorite_list.remove(event.message.text[5:])
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="成功刪除對象:"+event.message.text[5:]))

                elif re.match("尋找話題:", event.message.text):
                    flex_message3=carousel_list(topic,topic1,topic2,topic3)
                    line_bot_api.reply_message(event.reply_token, flex_message3)

                elif re.match("目前好感度:", event.message.text):
                    content = draw(imgur_client,attribute)
                    message = ImageSendMessage(original_content_url=content,preview_image_url=content)
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.text == '使用者':
                    user_id = event.source.user_id
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_id))

                else:
                    line_bot_api.reply_message(  # 回覆傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text="請輸入有效指令"))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()




