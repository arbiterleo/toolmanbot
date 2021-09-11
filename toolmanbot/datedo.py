from linebot.models import (
    ButtonComponent,
    TextComponent,
    SeparatorComponent,
    BubbleContainer,
    BoxComponent,
    MessageAction
    )

def datedo_list_generator(date):
    button_list = [BoxComponent(
                    layout="vertical",
                    margin="sm",
                    spacing="sm",
                    contents=[
                        TextComponent(text=date, weight="bold", size="xxl", margin="sm", wrap=True,),
                        SeparatorComponent(margin = "xl")

                        #好感度Button
                        ,ButtonComponent(style="primary", color="#ff80bb", size="md",height="md" ,margin="lg",
                                       action=MessageAction(label="目前好感度", text='目前好感度:'+date), )

                        #上傳對話Button(傳送user ID、對話紀錄，提醒後端接收)
                        ,ButtonComponent(style="primary", color="#ff80bb", size="md",height="md" ,margin="lg",
                                       action=MessageAction(label="上傳新的對話", text='請開始上傳對話:'+date), )

                        #尋找話題Button(傳送user ID，要求回傳top話題list)
                        ,ButtonComponent(style="primary", color="#ff80bb", size="md",height="md" ,margin="lg",
                                       action=MessageAction(label="尋找話題", text='尋找話題:'+date), )
                    ])]

    bubble=BubbleContainer(director='ltr',body=BoxComponent(layout="vertical",contents=button_list))


    return bubble