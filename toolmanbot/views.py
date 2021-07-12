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

#from dynamic_list_generator import favorite_list_generator
import json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

favorite_list=['小美','小花']

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
                    flex_message1=FlexSendMessage(alt_text='最愛清單',contents=favorite_list_generator(favorite_list))
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="jsadioashjdosajdo"))

                elif event.message.text == '搜尋對象':
                    FlexMessage = json.load(open('love_list.json','r',encoding='utf-8'))
                    line_bot_api.reply_message(event.reply_token, FlexSendMessage("對象1:"+favorite_list[0],FlexMessage))

                else:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                    )



        return HttpResponse()
    else:
        return HttpResponseBadRequest()


#dynamic_list_generator
def favorite_list_generator(favorite_list):

    button_list = [BoxComponent(
                    layout="vertical",
                    margin="sm",
                    spacing="sm",
                    content=[
                        TextComponent(text="最愛清單", weight="bold", size="md", margin="sm", wrap=True,),
                        SeparatorComponent(margin = "xl")
#                        ,ButtonComponent(style="primary", color="#997B66", size="md", margin="sm",
#                                        action=MessageAction(label="+", text='請輸入對象名字'), )
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
        direction='ltr',

        body=BoxComponent(
            layout="vertical",
            contents=button_list
        )
    )


