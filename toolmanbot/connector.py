import pymysql
import time
import datetime as dt

# 資料庫設定
db_settings = {
    "host": "database-1.c5ujpdahvdo6.us-east-2.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": "Goblin87!",
    "db": "try",
    "charset": "utf8"
}

def addUser(lineId):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "INSERT INTO user(lineId)VALUES(%s)"

            cursor.execute(command, (lineId))

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)

"""def addUser(id, name, lineId):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "INSERT INTO user(idUser, UserName, lineId)VALUES(%s, %s, %s)"

            cursor.execute(command, (id, name, lineId))

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)"""

def addChattingObject(name, userId):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "INSERT INTO chatting_object(objectName, User_lineId)VALUES(%s, %s)"

            cursor.execute(command, (name, userId))

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)

def addRecord(lineId,objectname):
    try:
        id = selectChattingObjectIdByUserLineIdandName(lineId,objectname)
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "INSERT INTO record(recordDate, chatting_object_idchatting_object)VALUES(%s, %s)"
            date = dt.date.today()
            datetime = "{}-{}-{}".format(date.year,date.month,date.day)
            cursor.execute(command, (datetime, id))

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)

def selectUserByUserId(id):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "SELECT * FROM user WHERE idUser = (%s)"

            cursor.execute(command, (id))
            return cursor.fetchall()

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)

def selectChattingObjectByUserLineId(id):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "SELECT * FROM chatting_object WHERE User_lineId = (%s)"

            cursor.execute(command, (id))

            result = cursor.fetchall()
            print(result)
            return result

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)

def selectChattingObjectIdByUserLineIdandName(id,name):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "SELECT idchatting_object FROM chatting_object WHERE User_lineId = (%s) AND objectName = (%s)"

            cursor.execute(command, (id,name))

            result = cursor.fetchall()
            return result[0][0]

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)


def selectChattingObjectNameByUserLineId(id):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "SELECT objectName FROM chatting_object WHERE User_lineId = (%s)"

            cursor.execute(command, (id))

            result = cursor.fetchall()
            print(result)
            return result

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)

#只會給你日期最晚的紀錄
def selectRecordByChattingObjectId(id):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "SELECT * FROM record WHERE chatting_object_idchatting_object = (%s) ORDER BY recordDate DESC"

            cursor.execute(command, (id))
            result = cursor.fetchone()
            return result[2:8]

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)


def getScoreByUserLineIdAndChattingObjectName(id,name):
    date = selectChattingObjectByUserLineId(id)
    for i in range(0,len(date)):
        if(date[i][1] == name):
            print(selectRecordByChattingObjectId(date[i][0]))
            return selectRecordByChattingObjectId(date[i][0])
    
    return "搜尋不到"

def getAvg():
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "SELECT * FROM total_avg WHERE id = 1"

            cursor.execute(command)
            result = cursor.fetchone()
            print(result[1:7])
            return result[1:7]

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)



def DeleteRecordByChattingObjectId(id):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "DELETE FROM record WHERE chatting_object_idchatting_object = (%s)"
            cursor.execute(command, (id))
            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)

addRecord("Uc294f08279daf51cd9b283228fbb9328","4C")
#addUser("testlineId")
#addChattingObject("Amy","testlineId")
#addRecord(10,dt.date(2021,9,1))
#selectUserByUserId("1")
#selectChattingObjectNameByUserLineId("Uc294f08279daf51cd9b283228fbb9328")
#getScoreByUserLineIdAndChattingObjectName("Uc294f08279daf51cd9b283228fbb9328","小美")
#selectRecordByChattingObjectId("8")
#getAvg()

