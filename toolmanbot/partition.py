# -*- coding: utf-8 -*-
#import ch
import jieba
import jieba.analyse
import jieba.posseg as pseg
import re
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# 範例

# text1 = '我最近和我朋友都在看籃球'

# print('\n- 斷字:\n\n', '|'.join(jieba.cut(text1, cut_all=False, HMM=True))+'\n')

# words = pseg.cut(text1)
# for word, flag in words:
#     print(word, flag)

findDate = re.compile(r'(\d\d\d\d)/([0-9]+)/([0-9]+)') #用來取出日期時間的regex
findTime = re.compile(r'(\d\d):(\d\d)')

def partition(text):

    # jump = 0
    keyword = []

    # 冗詞

    ignore = ['照片', '貼圖', '晚安', '早安', '感覺', '時候', '結果', '嘴巴', '檔案',
              '電話', '話', '樓', '意思', '原本', '大家', '時間', '眼', '人', '小夜', '電', '通話']

    # 把通話及照片的相關字句刪掉

    for Line in text:
        if '☎' in Line:
            # jump = 1
            return None

    # 自定義部分詞彙

    jieba.load_userdict('./data/userDict.txt')

    # 斷字結果

    # if jump == 0:
    #     result = jieba.cut(text, cut_all=False, HMM=True)
    #     print('|'.join(result))

    # 關鍵字抽取

    tags = jieba.analyse.extract_tags(text, topK=8)

    # 找出合適關鍵字

    str = ''
    temp = str.join(tags)

    words = pseg.cut(temp)
    for word, flag in words:
        ignore_set = set(ignore)
        if not word in ignore_set:
            if flag == ('n' or 'nr' or 'ns' or 'nt' or 'nz'):
                keyword.append(word)

    return keyword

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
    i = 0
    while name1[i] != "與":
        i += 1
    name1 = name1[i+1:]
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
    print(average, count, day)

    average = float(average/count)    #平均一次即時聊天的句數
    chatrate = float(count/day)     #平均一天即時聊天的次數
    final_score = (average + chatrate) * 1.79
    if final_score > 17.9:
        final_score = 17.9
    print("聊天頻率:", average, chatrate, final_score)

    f.close()
    return final_score

# 文字分析 + 回傳最後時間
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
    i = 0
    while name[i] != "與":
        i += 1
    name = name[i+1:]
    chat_record = all_lines[3:]
    len1 = 6 + len(name)
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