import ch
import call as ca


def callr(file):

    record = ca.capture(file)
    # print(record)

    calltime = ca.callTime(record, 99)  # 傳回帶有日期的通話時間，追溯前99天(共有100天)

    callrate = ca.callRate(calltime)
    # print(callrate) # 頻率變化

    print('\n100天的通話頻率 : ', len(calltime), '\n')  # 兩禮拜內的通話數

    RateScore = ca.callrScore(callrate)

    return RateScore
