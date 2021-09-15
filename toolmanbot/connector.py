import pymysql
import time
import datetime as dt

# 資料庫設定
db_settings = {
    "host": "35.194.247.117",
    "port": 3306,
    "user": "admin01",
    "password": "testbot123",
    "db": "e_line",
    "charset": "utf8"
}

def addUser(id, name, lineId):
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
        print(ex)

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

def addRecord(id,date):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "INSERT INTO record(recordDate, chatting_object_idchatting_object)VALUES(%s, %s)"
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
            print(cursor.fetchall())

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
            return cursor.fetchall()

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
            print(result[2:8])

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

    except Exception as ex:
        print(ex)

# USER ID 搜尋得分
def getRecordScore(id, ScoreName):
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "SELECT " + ScoreName + \
                " FROM record WHERE idrecord = (%s)"

            cursor.execute(command, (id))

            # 儲存變更
            conn.commit()

        # 關閉connection
        conn.close()

        return cursor.fetchone()

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


#addRecord(8,dt.date(2022,8,9))
#selectUserByUserId("1")
selectChattingObjectByUserLineId("Uc294f08279daf51cd9b283228fbb9328")
selectRecordByChattingObjectId("8")

