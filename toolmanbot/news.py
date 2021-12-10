from bs4 import BeautifulSoup
import requests
import time
from random import randint


def scrape_news_summaries(s):
    time.sleep(randint(0, 2))  # relax and don't let google be angry
    record = False

    r = requests.get("http://www.google.co.uk/search?q="+s+"&tbm=nws")

    # print("\nurl: http://www.google.co.uk/search?q=" + s +"&tbm=nws")

    # 伺服器回應的狀態碼
    # print(r.status_code)

    content = r.text
    news_summaries = []
    soup = BeautifulSoup(content, "html.parser")

    keys = soup.findAll("a")

    for k in keys:
        if k.text == "下一頁 >":
            record = False  # 紀錄停止
        if record:
            news_summaries.append(k.text.strip() + "\n\n" + k.get("href"))
        if k.text == "按日期排序":
            record = True  # 代表開始記錄新聞

    str = '/url?'

    # 去掉多餘的值
    for item in news_summaries:
        if str in item[0:7]:
            news_summaries.remove(item)

    return news_summaries
