import re
import datetime as dt
#import connector as ct

#------------------------------變數設定---------------------------------
#chatfile = open('[LINE] 與好感度救星的聊天.txt', mode='r', encoding="utf-8")
#chatfile = open('test_file.txt', mode='r', encoding="utf-8")

#chat = chatfile.readlines()

#user = "緯"
#target = "好感度救星"

isUser = None

#計算回覆量分數的標準
amountArr = [5,15]
amountScoreArr = [67,90]

#計算回覆量分數的標準
speedArr = [600,300,60,30,10]
speedScoreArr = [8.9,17.4,53.7,70.3,98.8]

findDate = re.compile(r'(\d\d\d\d)/([0-9]+)/([0-9]+)') #用來取出日期時間的regex
findTime = re.compile(r'(\d\d):(\d\d)')

#-------------------------------function----------------------------------
def findTargetName(chat):
    line = chat[0][8:]
    return line[0:len(line)-6]

def findUserName(chat):
    for i in range(3,len(chat)-1):
        if(chat[i][2] == ":"):
            if(chat[i][6:5 +len(findTargetName(chat))]!= findTargetName(chat)):
                j = 6
                name = ""
                while chat[i][j].isspace() == False:
                    name += chat[i][j]
                    j+=1
                return name

    return "error"

def checkIfChat(line,user,target):
    line = line[6:]

    mo = re.match(user, line)
    if mo != None:
        return 1 #this line is said by user
    else:
        mo = re.match(target, line)
        if mo != None:
            return 2 #this line is said by target
        else:
            return 0 #this line isn't conversation

def checkIfReplied(line,user,target):
    global isUser
    result = checkIfChat(line,user,target)
    if result == 1:
        if not isUser:
            isUser = True
            return 2 #the respones from target ends here
        else:
            return 0 #this line is said by user, no need to take action

    elif result == 2:
        if isUser:
            isUser = False
            return 1 #this line is the first response by target, needs to ba added into the amount, also needs to calculate the response time
        else:
            return 3 #this line is said by target, needs to ba added into the amount

    else:
        return 0 #this line isn't conversation, no need to take action

def calculate_speed(chat):
    user = findUserName(chat)
    target = findTargetName(chat)

    date = []
    totalResponseTime = dt.timedelta()
    count = 0

    for i in range(3, len(chat)-1): #and chat[i].strip() != ""
        if checkIfChat(chat[i],user,target) == 0 and findDate.search(chat[i]) != None: #將檔案中的空白行去掉
            date.append(chat[i])
        elif checkIfReplied(chat[i],user,target) == 1:
            temp = checkIfChat(chat[i-1],user,target)
            if  (temp == 0 and findDate.search(date[len(date)-2]) != None and findDate.search(date[len(date)-1])!= None):
                userdate = findDate.search(date[len(date)-2])
                usertime = findTime.search(chat[i-3])
                targetdate = findDate.search(date[len(date)-1])
                targettime = findTime.search(chat[i])
                userdatetime = dt.datetime(int(userdate.group(1)), int(userdate.group(2)), int(userdate.group(3)),int(usertime.group(1)), int(usertime.group(2)))
                targetdatetime = dt.datetime(int(targetdate.group(1)), int(targetdate.group(2)), int(targetdate.group(3)),int(targettime.group(1)), int(targettime.group(2)))
                print("responsetime:", targetdatetime-userdatetime, i)
            elif (temp == 1 and findDate.search(date[len(date)-1])!= None and findDate.search(date[len(date)-1])!= None):
                userdate = findDate.search(date[len(date)-1])
                usertime = findTime.search(chat[i-1])
                targetdate = findDate.search(date[len(date)-1])
                targettime = findTime.search(chat[i])
                userdatetime = dt.datetime(int(userdate.group(1)), int(userdate.group(2)), int(userdate.group(3)),int(usertime.group(1)), int(usertime.group(2)))
                targetdatetime = dt.datetime(int(targetdate.group(1)), int(targetdate.group(2)), int(targetdate.group(3)),int(targettime.group(1)), int(targettime.group(2)))
                #print("responsetime:", targetdatetime-userdatetime, i)

            totalResponseTime += (targetdatetime-userdatetime)
            count += 1
        #else:
            #print("對話行:", i)
    print("平均每次回覆時間:", totalResponseTime/count)

    lastdate = dt.date(int(userdate.group(1)), int(userdate.group(2)), int(userdate.group(3)))
    #ct.DeleteRecordByChattingObjectId("8")
    #ct.addRecord("8",lastdate)

    return totalResponseTime/count

def calculate_amount(chat):
    global isUser
    count = 0
    amount = 0
    user = findTargetName(chat)
    target = findUserName(chat)

    for line in chat:
        result = checkIfReplied(line,user,target)
        if result == 1 or result == 3:
            amount += (len(line)-11)
        elif result == 2:
            count += 1

    isUser = None #還原初值避免下次運算出錯
    return (amount/count)

def getWheretoStart(lastdate,path):
    chatfile = open(path, mode='r', encoding="utf-8")
    chat =chatfile.readlines()

    for i in range(len(chat)-1, 3, -1):
        result = findDate.search(chat[i])
        if(result != None):
            currentdate = dt.date(int(result.group(1)),int(result.group(2)),int(result.group(3)))
            if(currentdate == lastdate):
                return i
    return -1

def getAmountScore(path):
    chatfile = open(path, mode='r', encoding="utf-8")
    chat =chatfile.readlines()

    amount = calculate_amount(chat)
    #print(amount)
    if(amount < amountArr[0]):
        return amountScoreArr[0]*(amount/amountArr[0])
    elif(amount < amountArr[1]):
        return amountScoreArr[0] + (amountScoreArr[1] - amountScoreArr[0])*((amount-amountArr[0])/(amountArr[1]-amountArr[0]))
    else:
        return 99

def getSpeedScore(path):
    chatfile = open(path, mode='r', encoding="utf-8")
    chat =chatfile.readlines()

    speed = calculate_speed(chat).total_seconds()
    #print(speed)
    if(speed > speedArr[0]):
        return speedScoreArr[0]
    elif(speed > speedArr[1]):
        return speedScoreArr[1]
    elif(speed > speedArr[2]):
        return speedScoreArr[2]
    elif(speed > speedArr[3]):
        return speedScoreArr[3]
    elif(speed > speedArr[4]):
        return speedScoreArr[4]
    else:
        return 100

#--------------------------------測試區------------------------------------------


#print("回復量分數:",getAmountScore('[LINE] 與好感度救星的聊天.txt'))
#print("速度分數:",getSpeedScore('[LINE] 與好感度救星的聊天.txt'))

#print("斷點:",getWheretoStart(dt.date(2021,9,15),'[LINE] 與好感度救星的聊天.txt'))


#chatfile.close()