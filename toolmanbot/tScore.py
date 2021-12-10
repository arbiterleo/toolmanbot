import ch
import call as ca


def callt(file):

    record = ca.capture(file)
    # print(record)

    calltime = ca.callTime(record, 99)  # 傳回帶有日期的通話時間，追溯前99天(共有100天)
    call = ca.callTime(record, 7)

    print('\n', calltime)

    history = ca.callAvgTime(calltime)  # 100天的歷史總時間平均

    print('\n歷史通話平均時間(分鐘) : ', history)

    return ca.callScore(call, history)
