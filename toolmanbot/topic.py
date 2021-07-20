from linebot.models import (
    ButtonComponent,
    TextComponent,
    SeparatorComponent,
    BubbleContainer,
    CarouselContainer,
    BoxComponent,
    MessageAction
    )

def topic_carousel(topic):
    carousel_list=[]
    for i in len(topic):
        button_list = [BoxComponent(
                    layout="vertical",
                    margin="sm",
                    spacing="sm",
                    contents=[
                        TextComponent(text=topic[i], weight="bold", size="xxl", margin="sm", wrap=True,),
                        SeparatorComponent(margin = "xl")

                        #Button
                        ,ButtonComponent(style="primary", color="#ff80bb", size="md",height="md" ,margin="lg",
                                       action=MessageAction(label="測試", text=topic+':測試'), )

                    ])]

        bubble=BubbleContainer(
                    director='ltr',
                    body=BoxComponent(layout="vertical",contents=button_list
                    )
                )
        carousel_list.append(bubble)

    carousel=CarouselContainer(contents=carousel_list

    )






