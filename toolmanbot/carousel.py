from linebot.models import FlexSendMessage

def carousel_list(topic):
  flexmessage3=FlexSendMessage(
    alt_text="carousel",
    contents={
      "type": "carousel",
    "contents": [
      {
        "type": "bubble",

        "header": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": topic[0], #主題1
              "size": "xxl",
              "margin": "none"
            },
            {
              "type": "separator",
              "margin": "md"
            }
          ]
        },
        "hero": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "解釋topic1顯示原因"
            }
          ]
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic1相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic1相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic1相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            }
          ]
        }
      },
      {
        "type": "bubble",
        "header": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": topic[1], #主題2
              "size": "xxl",
              "margin": "none"
            },
            {
              "type": "separator",
              "margin": "md"
            }
          ]
        },
        "hero": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "解釋topic2顯示原因"
            }
          ]
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic2相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic2相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic2相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            }
          ]
        }
      },
      {
        "type": "bubble",
        "header": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": topic[2], #主題3
              "size": "xxl",
              "margin": "none"
            },
            {
              "type": "separator",
              "margin": "md"
            }
          ]
        },
        "hero": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "解釋topic3顯示原因"
            }
          ]
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic3相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic3相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic3相關時事主題",
                "uri": "https://www.youtube.com/channel/UC0C-w0YjGpqDXGB8IHb662A"
              }
            }
          ]
        }
      }
    ]
  }
)
  return flexmessage3