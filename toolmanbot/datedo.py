def datedo_list_generator(date):
    button_list = [BoxComponent(
                    layout="vertical",
                    margin="sm",
                    spacing="sm",
                    contents=[
                        TextComponent(text="對象："+date, weight="bold", size="md", margin="sm", wrap=True,),
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