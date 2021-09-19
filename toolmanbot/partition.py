import re
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

findDate = re.compile(r'(\d\d\d\d)/([0-9]+)/([0-9]+)') #用來取出日期時間的regex
findTime = re.compile(r'(\d\d):(\d\d)')


#算頻率(目前只有一句對話的區間不會等於沒有聊天，但count會被+1)
#input: 檔案位址， return:對話頻率分數(最高17.9)
def frequency(file_addr):
    day = 0   #用以計算天數
    live_chat_count = 0   #計算這次的即時對話目前幾行(其實目前不需要但是先放著以備不時之需)
    count = 0   #算一天即時對話的次數，在此我以10分鐘內算即時
    average = 0   #算平均即時對話的句數

    f = open(file_addr, "r", encoding="utf-8")
    all_lines = f.readlines()
    name1 = all_lines[0][:-6]
    name1 = name1[9:]
    chat_record = all_lines[3:]
    len1 = 6 + len(name1) + 1
    print(chat_record[2][6:len1])

    #以下開始計算頻率
    last_date = findDate.search(chat_record[0])
    last_year = int(last_date.group(1))     #上一年
    last_month = int(last_date.group(2))    #上一月
    last_day = int(last_date.group(3))      #上一日
    last_word = chat_record[1][:-1]    #紀錄上一個對話

    for words in chat_record:
        if len(words) > 2:    #有時候會突然出現空白行
            if findDate.search(words) != None:   #如果跨日
                now_date = findDate.search(words)
                now_year = int(now_date.group(1))
                now_month = int(now_date.group(2))
                now_day = int(now_date.group(3))
                day += (now_year - last_year)*365 + (now_month - last_month)*30 + (now_day - last_day)
                last_year = now_year
                last_month = now_month
                last_day = now_day
            elif findTime.search(words[0:5]) != None: #words[2] == ':':
                hour_gap =  int(words[0:2]) - int(last_word[0:2])
                miunte_gap = int(words[3:5]) - int(last_word[3:5])
                if (hour_gap == 0 and miunte_gap <= 10) or (hour_gap == 1 and abs(miunte_gap) >= 55):
                    if words[6:len1] != last_word[6:len1]:
                        live_chat_count += 1
                else:
                    average += live_chat_count
                    live_chat_count = 0
                    count += 1

                last_word = words

    #最後再把迴圈沒算到的最後一次對話區間加進來
    average += live_chat_count
    live_chat_count = 0
    count += 1

    average = float(average/count)    #平均一次即時聊天的句數
    chatrate = float(count/day)     #平均一天即時聊天的次數 ######################
    final_score = (average + chatrate) * 1.79
    if final_score > 17.9:
        final_score = 17.9
    print(average, chatrate, final_score)

    f.close()
    return final_score

# 文字分析
def authenticate_client():
    ta_credential = AzureKeyCredential('088f06feefd842fcabc7a17bc0005c0f')
    text_analytics_client = TextAnalyticsClient(
        endpoint='https://12341234.cognitiveservices.azure.com/',
        credential=ta_credential)
    return text_analytics_client


client = authenticate_client()

def sentiment_analysis_example(client, documents):
    response = client.analyze_sentiment(documents=documents)[0]
    return response.confidence_scores

#文字分析主功能
#input:檔案位址，return:好感度分數(最高19.2)
def wordanalysis(file_addr):
    f = open(file_addr, "r", encoding="utf-8")
    all_lines = f.readlines()
    name = all_lines[0][:-6]
    name = name[9:]
    chat_record = all_lines[3:]
    len1 = 6 + len(name) + 1
    documents = []
    positive = 0
    neutral = 0
    negative = 0
    count = 0
    for words in chat_record:
        if words[6:len1] == name:
            documents = [{
                "language": "zh-hant",
                "id": "1",
                "text": words[9:]
            }]
            score = sentiment_analysis_example(client, documents)

            positive += score.positive
            neutral += score.neutral
            negative += score.negative
            count = count + 1

    positive /= count
    neutral /= count
    negative /= count
    print(positive, neutral, negative)
    final_score = (positive - negative + 1) * 19.2 / 2
    print(final_score)

    f.close()
    return final_score


#a=frequency('/Users/xwlee/Downloads/[LINE] 與好感度救星的聊天.txt')
#print(a)