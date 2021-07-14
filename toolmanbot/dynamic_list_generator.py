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

def favorite_list_generator(favorite_list):
    button_list = [BoxComponent(
                    layout="vertical",
                    margin="sm",
                    spacing="sm",
                    contents=[
                        TextComponent(text="最愛清單", weight="bold", size="xxl", margin="sm", wrap=True,),
                        SeparatorComponent(margin = "xl")
                        ,ButtonComponent(style="primary", color="#ff66a3", size="md", margin="sm",
                                       action=MessageAction(label="+", text='開始新增對象，請輸入「新增對象：對象名稱」'), )
                    ])]

    for i in favorite_list:

        favorite_button = ButtonComponent(style="primary", color="#ff66a3", size="sm", margin="sm",
                                        action=MessageAction(label=i, text=f'搜尋對象：{i}'),)
        delete_button=ButtonComponent(style="secondary", color="#ff3333", size="sm", margin="sm", flex=0,
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