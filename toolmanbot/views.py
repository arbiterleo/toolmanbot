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
    ButtonComponent,
    TextComponent,
    SeparatorComponent,
    BubbleContainer,
    BoxComponent,
    MessageAction
)

#from .dynamic_list_generator import favorite_list_generator
def favorite_list_generator(favorite_list):
    button_list = [BoxComponent(
                    layout="vertical",
                    margin="sm",
                    spacing="sm",
                    contents=[
                        TextComponent(text="最愛清單", weight="bold", size="md", margin="sm", wrap=True,),
                        SeparatorComponent(margin = "xl")
                        ,ButtonComponent(style="primary", color="#997B66", size="md", margin="sm",
                                       action=MessageAction(label="+", text='開始新增對象，請輸入「新增對象：對象名稱」'), )
                    ])]

    for i in favorite_list:

        favorite_button = ButtonComponent(style="primary", color="#997B66", size="sm", margin="sm",
                                        action=MessageAction(label=i, text=f'搜尋對象：{i}'),)
        delete_button=ButtonComponent(style="secondary", color="#F1DCA7", size="sm", margin="sm", flex=0,
                                      action=MessageAction(label="-", text="刪除對象："+i), )
        button_row=BoxComponent(layout="horizontal", margin="md", spacing="sm",
                                contents=[favorite_button, delete_button])
        button_list.append(button_row)


    bubble=BubbleContainer(
                    director='ltr',
                    body=BoxComponent(layout="vertical",contents=button_list
                    )
                )
    return bubble
#from .datedo import datedo_list_generator
def datedo_list_generator(date):
    button_list = [BoxComponent(
                    layout="vertical",
                    margin="sm",
                    spacing="sm",
                    contents=[
                        TextComponent(text=date, weight="bold", size="xxl", margin="sm", wrap=True,),
                        SeparatorComponent(margin = "xl")
                        ,ButtonComponent(style="primary", color="#ff80bb", size="md",height="md" ,margin="lg",
                                       action=MessageAction(label="目前好感度", text=date+'目前好感度'), )

                        ,ButtonComponent(style="primary", color="#ff80bb", size="md",height="md" ,margin="lg",
                                       action=MessageAction(label="上傳新的對話", text='請開始上傳對話：'+date), )

                        ,ButtonComponent(style="primary", color="#ff80bb", size="md",height="md" ,margin="lg",
                                       action=MessageAction(label="尋找話題", text='尋找話題：'+date), )
                    ])]
    bubble=BubbleContainer(
                    director='ltr',
                    body=BoxComponent(layout="vertical",contents=button_list
                    )
                )
    return bubble

import json
import re


line_bot_api = LineBotApi('e93603f23a91577079b4444b359ded8a')
parser = WebhookParser('PEgvXyP6nPE8lIgLXAIz2D7Q3xNs4WLNHkELlarlhvBP85r/FnjLSnE+EKVp5reuNstda/i0yWXD0Tbe2IUWyqR3c6ws1t9HK4KIu9jfKS6bC7N2A1M6bLU1jm4Ukd4B4sn5pkj9A4RQgm6ENu3GKgdB04t89/1O/w1cDnyilFU=')

favorite_list=['小美','小花']
date=favorite_list[0]
a=datedo_list_generator(date)

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

        for event in events:

            if isinstance(event, MessageEvent):  # 如果有訊息事件

                if event.message.text == '最愛清單':
                    favorite_list_button=favorite_list_generator(favorite_list)
                    flex_message1=FlexSendMessage(alt_text='最愛清單',contents=favorite_list_button)
                    line_bot_api.reply_message(event.reply_token, flex_message1)

                elif event.message.text == "搜尋對象："+ date:
                    flex_message2=FlexSendMessage(alt_text=favorite_list[0],contents=a)
                    line_bot_api.reply_message(event.reply_token, flex_message2)

                elif re.match("新增對象：", event.message.text):
                    favorite_list.append(event.message.text[5:])
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="成功新增對象："+event.message.text[5:]))
                    print(favorite_list)

                elif event.message.text == '最愛清單測試':
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=favorite_list[-1]))

                else:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()




