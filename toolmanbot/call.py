# coding:utf-8
import ch
import datetime
import connector as conn

keystr = '通話時間'


end = datetime.date.today().strftime('%Y/%m/%d')
start = (datetime.date.today() +
         datetime.timedelta(days=-99)).strftime('%Y/%m/%d')


def capture(record):
    r = []  # 回傳值

    print('從', start, '追蹤至', end, '\n')

    # 從最新的資料往前追蹤
    with open(record, 'r', encoding="utf-8") as f:
        for line in reversed(f.readlines()):
            r.append(line)
            if line[0: 10] == start:
                break
    f.close

    return r


def callTime(record, day):
    time = {}
    date = datetime.date.today() - datetime.timedelta(day)  # 通話日期
    d_phone = date.strftime('%Y/%m/%d')  # 通話的期的字串格式
    d_flag = d_phone  # 當作比對日期的變數並傳給 d_phone
    flag = 0

    d = int(d_flag[0:4])
    e = int(d_flag[5:7])
    f = int(d_flag[8:10])

    for callLine in reversed(record):

        if callLine.find("週") == -1:
            if callLine.count('/') == 2 and callLine.find("/") != -1 and callLine.find("/") == 4:

                a = int(callLine[0:4])
                b = int(callLine[5:7])
                c = int(callLine[8:10])

                if (a > d) or (a == d and b > e) or (a == d and b == e and c >= f):
                    d_phone = callLine[0:10]
                    # date = date + datetime.timedelta(days=1)
                    # d_flag = date.strftime('%Y/%m/%d')
                    flag = 1
        else:
            if callLine.count('/') == 2 and callLine.find("/") != -1 and callLine.find("/") == 4:

                a = int(callLine[0:4])
                b = int(callLine[callLine.find("/")+1:callLine.rfind("/")])
                c = int(callLine[callLine.rfind("/")+1:callLine.find("(")-4])

                if (a > d) or (a == d and b > e) or (a == d and b == e and c >= f):
                    d_phone = callLine[0:4] + "/" + \
                        callLine[callLine.find(
                            "/")+1:callLine.rfind("/")].zfill(2) + "/" + callLine[callLine.rfind("/")+1:callLine.find("(")-4].zfill(2)
                    # date = date + datetime.timedelta(days=1)
                    # d_flag = date.strftime('%Y/%m/%d')
                    flag = 1

        if keystr in callLine and flag == 1:
            time[d_phone] = (callLine[callLine.index(keystr)+4: -1])
            flag = 0

    return time


def callAvgTime(time):
    avg = []
    flag = 1
    second = 0
    temp = 0  # 通話時間加總的暫存

    # 計算每7次的平均通話
    for t_phone in reversed(tuple(time.values())):

        t_list = t_phone.split(':')  # 將字串分割成小時/分鐘/秒的 List
        i = 1

        for t in range(len(t_list)-1, -1, -1):
            second = second + int(t_list[t])*i  # 轉成整數並計算總秒數
            i *= 60
        temp = temp + second

        # 加總7次通話
        if flag % 7 == 0:
            avg.append(temp//7//60)  # 換成分鐘
            temp = 0
        second = 0
        flag += 1

        total = 0
        for s in avg:
            total += s

    return total


def callScore(time, history):
    avg = 0
    second = 0
    temp = 0  # 通話時間加總的暫存

    # 計算7次的平均通話
    for t_phone in reversed(tuple(time.values())):

        t_list = t_phone.split(':')  # 將字串分割成小時/分鐘/秒的 List
        i = 1

        for t in range(len(t_list)-1, -1, -1):
            second = second + int(t_list[t])*i  # 轉成整數並計算總秒數
            i *= 60
        temp = temp + second

        # 加總7次通話
        avg = temp//7//60  # 換成分鐘
        second = 0

    # 計算得分
    gap = 0  # 此次分數
    score = 80  # 上次分數

    print('\n此次平均通話(分鐘) : ', avg)

    # 比較歷史紀錄
    if avg < history:  # 退步
        m = (avg - history)*5  # 分鐘變化量為5分
        if m < -50:
            gap = 0
        else:
            gap = score-m
    elif avg > history:  # 進步
        m = (avg - history)*5
        if m > 50:
            gap = 100
        else:
            gap = score+m

    score = ((7-1)*score + 1*gap)//7  # 6:1

    return score


def callRate(record):
    w = 0
    week = []  # 各禮拜通話頻率(共100筆)

    s = int(start[8:])  # 起始日期
    e = int(end[8:])    # 結束日期

    sm = int(start[5: 7])  # 現在月份
    em = int(end[5: 7])

    # 每一禮拜紀錄一次

    while sm <= em:

        if s > e and sm == em:
            break

        print(sm, s, '-> ', end='')
        c = 0  # 各禮拜通話的暫存次數
        if (sm/2 == 0 or sm == 7) and sm != 2:  # 大月份且不是2月
            if s+6 > 31:
                sm += 1
                s = s+6-31
            else:
                s += 6
        elif sm == 2:  # 2月(不管閏月)
            if s+6 > 28:
                sm += 1
                s = s+6-28
            else:
                s += 6
        else:  # 小月份
            if s+6 > 30:
                sm += 1
                s = s+6-30
            else:
                s += 6

        print(sm, s)
        for d in record.keys():
            s2 = int(d[8:])  # 每次通話的日期
            m2 = int(d[5: 7])  # 每次通話的月份

            s2e = int(list(record.keys())[-1][8:])
            m2e = int(list(record.keys())[-1][5: 7])  # 最後一次通話的月份

            if m2 < sm:  # 曾經通話月份 < 當次結束月份，則次數c+1
                c += 1
                if m2 == m2e and s2 == s2e and w != 0:  # 這次的通話為100天內的最後一次且已有紀錄
                    week.append(c-w)
                    print(4, c, w)
                    break
                elif w == 0:
                    week.append(0)
                    print(5)
                    break
            elif m2 == sm:    # 月份相同比日期
                if s2 < s:    # 曾經通話日期 < 當次結束日期
                    c += 1

                    if m2 == m2e and s2 == s2e and w != 0:  # 這次的通話為100天內的最後一次且已有紀錄
                        week.append(c-w)
                        print(1)
                        break
                    elif w == 0:
                        week.append(c)
                        w = c
                        print(2)
                        break

                elif s2 == s:  # 有通話的時間剛好在當次最後一天
                    c += 1

                    if m2 == m2e and s2 == s2e and w != 0:  # 這次的通話為100天內的最後一次且已有紀錄
                        week.append(c-w)
                        break
                    elif w == 0:
                        week.append(0)
                        break

                else:          # 月份相同但通話日期比較晚，代表之後的通話都不在此範圍
                    week.append(c-w)
                    print(3)
                    w = c      # 總次數
                    break
            else:              # 此次結束月份 < 通話月份
                week.append(c-w)
                # print(0)
                break

            if c == 0:
                week.append(0)
                print(4)
                break

            week.append(c-w)
            break

    return week


def callrScore(rate):
    attend = 0  # -是退步 0是持平 +是進步
    avg = 0
    temp = rate[0]

    for r in rate:
        if temp < r:
            if avg > r:  # 雖然進步但低於平均
                attend -= 1
            elif avg < r:
                attend += 1
            avg = (avg + r)//2
            temp = r
            attend += 5  # 比上次好，進步趨勢5
            if attend > 20:
                attend = 20
            elif attend < -20:
                attend = -20

        elif temp > r:
            if avg > r:  # 退步且低於平均
                attend -= 1
            elif avg < r:
                attend += 1
            avg = (avg + r)//2
            temp = r
            attend -= 5  # 比上次差，退步趨勢5
            if attend > 20:
                attend = 20
            elif attend < -20:
                attend = -20

    print('此次趨勢程度 : ', attend)

    score = 70  # 假設上一次的分數
    score = int(((7-1)*score + 1*(1+(5*attend/100))*score)/7)  # 6:1

    return score
