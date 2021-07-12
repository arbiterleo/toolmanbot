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

from .dynamic_list_generator import favorite_list_generator
from .datedo import datedo_list_generator

import json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

favorite_list=['小美','小花']
favorite_list_button=favorite_list_generator(favorite_list)

a=datedo_list_generator(favorite_list[0])

@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件

                if event.message.text == '[[最愛清單]]':
                    flex_message1=FlexSendMessage(alt_text='最愛清單',contents=favorite_list_button)
                    line_bot_api.reply_message(event.reply_token, flex_message1)

                elif event.message.text == '搜尋對象'+favorite_list[0]:
                    flex_message2 = FlexSendMessage(alt_text='搜尋對象'+favorite_list[0],contents=a)
                    line_bot_api.reply_message(event.reply_token, flex_message2)

                else:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()




