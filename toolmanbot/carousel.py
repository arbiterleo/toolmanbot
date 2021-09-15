from linebot.models import FlexSendMessage

def carousel_list(topic,topic1,topic2,topic3):
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

        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic1相關時事主題",
                "uri": topic1[0] #topic1 連結1
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic1相關時事主題",
                "uri": topic1[1] #topic1 連結2
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic1相關時事主題",
                "uri": topic1[2] #topic1 連結3
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

        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic2相關時事主題",
                "uri": topic2[0] #topic2 連結1
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic2相關時事主題",
                "uri": topic2[1] #topic2 連結2
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic2相關時事主題",
                "uri": topic2[2] #topic2 連結3
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

        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic3相關時事主題",
                "uri": topic3[0] #topic3 連結1
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic3相關時事主題",
                "uri": topic3[1] #topic3 連結2
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "topic3相關時事主題",
                "uri":topic3[2] #topic3 連結3
              }
            }
          ]
        }
      }
    ]
  }
)
  return flexmessage3