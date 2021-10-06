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
from .connector import selectChattingObjectNameByUserLineId,addUser,addChattingObject,addRecord
from .partition import frequency


#登入linebot 跟 imgur 需要的東西(from settings)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
imgur_client=settings.IMGUR_CLIENT_ID


######需要從後端得到的東西######
#favorite_list=[] #最愛清單(from db)

values = [60,51,70,80,60,50] #各指標本次分數(from model)
values_a= [40,50,80,70,90,60] #各指標平均分數(from DB)

#本次分數
get_point_a=80.5
#上次分數
get_point_b=77.5

#把分數型態轉變為字串
point=str(get_point_a)
difference=str(get_point_a-get_point_b)

#話題主題前三名
topic=["Travel","Sports","Fashion"]

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

        global topic

        for event in events:

            if isinstance(event, MessageEvent):

                if event.message.type=='file': #############分析完後要回傳到資料庫##################
                    fname1=event.message.file_name[8:]
                    fname2=fname1[:-7]
                    user_id=event.source.user_id
                    file_path = f'/tmp/{user_id}:{fname2}'
                    message_content = line_bot_api.get_message_content(event.message.id)
                    with open(file_path, 'wb') as fd:
                        for chunk in message_content.iter_content():
                            fd.write(chunk)

                    #addRecord(user_id,fname2)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=file_path))

                elif re.match('檔案分數：', event.message.text):
                    file_path = f'/tmp/{event.source.user_id}:{event.message.text[5:]}'
                    a=frequency(file_path)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))

                elif event.message.text == '報表說明':
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = instrution_content()))

#####第一次使用需要註冊帳號######
                elif event.message.text == '我要註冊':
                    user_id = event.source.user_id
                    addUser(user_id)

#####查看分析名單######
                elif event.message.text == '分析名單':
                    user_id = event.source.user_id
                    tup=selectChattingObjectNameByUserLineId(user_id)
                    favorite_list=[]
                    for i in range(len(tup)):
                        favorite_list.append(tup[i][0])
                    favorite_list_button=favorite_list_generator(favorite_list)
                    flex_message1=FlexSendMessage(alt_text='分析名單',contents=favorite_list_button)
                    line_bot_api.reply_message(event.reply_token, flex_message1)

                elif re.match("搜尋對象:", event.message.text):
                    date=event.message.text[5:] # 對象名稱(date)
                    flex_message2=FlexSendMessage(alt_text=date,contents=datedo_list_generator(date))
                    line_bot_api.reply_message(event.reply_token, flex_message2)

#####新增對象######
                elif re.match("新增對象：", event.message.text):
                    name=event.message.text[5:]
                    user_id = event.source.user_id
                    addChattingObject(name,user_id)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="成功新增對象:"+event.message.text[5:]))

#####刪除對象#####還沒完成
                elif re.match("刪除對象:", event.message.text):
                    favorite_list.remove(event.message.text[5:])
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="成功刪除對象:"+event.message.text[5:]))

                elif re.match("尋找話題:", event.message.text):
                    flex_message3=carousel_list(topic,topic1,topic2,topic3)
                    line_bot_api.reply_message(event.reply_token, flex_message3)

######從資料庫抓1.最新分數＆次新分數陣列 2.最新指標＆次新指標陣列 3.平均指標######還沒完成
                elif re.match("目前好感度:", event.message.text):
                    reply_arr=[]
                    t_content=text_report(values,values_a)
                    txt=TextSendMessage(text=t_content)
                    reply_arr.append(txt)
                    i_content = draw(imgur_client,values,values_a,point,difference)
                    img=ImageSendMessage(original_content_url=i_content,preview_image_url=i_content)
                    reply_arr.append(img)
                    line_bot_api.reply_message(event.reply_token, reply_arr)

                elif re.match("開始新增對象，請輸入「新增對象：對象名稱」", event.message.text):
                   pass

                else:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入有效指令"))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()





