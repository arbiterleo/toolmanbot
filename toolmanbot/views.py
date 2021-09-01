from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

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
    MessageAction)

import re
import numpy as np
import matplotlib.pyplot as plt


#function
from .dynamic_list_generator import favorite_list_generator #最愛清單function
from .datedo import datedo_list_generator  #對象工具列
from .carousel import carousel_list
from .report import draw,text_report
from .TextTemplate import instrution_content


#登入linebot 跟 imgur 需要的東西(from settings)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
imgur_client=settings.IMGUR_CLIENT_ID


#需要從後端得到的東西
favorite_list=["小美","小花"] #最愛清單

values = [20,31,24,80,80,50] #各指標本次分數
values_p= [35,80,60,50,70,40] #各指標前次分數
values_a= [40,50,12,70,90,60] #各指標平均分數

get_point_a=80.5  #本次分數
get_point_b=77.5 #上次分數

point=str(get_point_a)
difference=str(get_point_a-get_point_b)

topic=["Travel","Sports","Fashion"] #話題主題前三名

#主題1新聞連結
topic1=["https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"]
#主題2新聞連結
topic2=["https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A",
        "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"]
#主題3新聞連結
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
        global fav

        for event in events:

            if isinstance(event, MessageEvent):  # 如果有訊息事件

                if event.message.text == '最愛清單':
                    favorite_list_button=favorite_list_generator(favorite_list)
                    flex_message1=FlexSendMessage(alt_text='最愛清單',contents=favorite_list_button)
                    line_bot_api.reply_message(event.reply_token, flex_message1)

                elif event.message.text == '報表說明':
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = instrution_content()))

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
                    reply_arr=[]
                    t_content=text_report(values,values_p)
                    txt=TextSendMessage(text=t_content)
                    reply_arr.append(txt)
                    i_content = draw(imgur_client,values,values_a,point,difference)
                    img=ImageSendMessage(original_content_url=i_content,preview_image_url=i_content)
                    reply_arr.append(img)
                    line_bot_api.reply_message(event.reply_token, reply_arr)

                elif event.message.text == '使用者':
                    user_id = event.source.user_id
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_id))

                else:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入有效指令"))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()




