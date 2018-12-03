import sqlite3 as lite


def getConnection():
    db_name = "minwon.db"
    return lite.connect(db_name)

def getCursor(conn):
    return conn.cursor()



def create_table():
    query = "CREATE TABLE IF NOT EXISTS minwon_infomation (id INTEGER PRIMARY_KEY NOT NULL, " \
            "name VARCHAR(255)"
    string =''
    args = ['과세대상', '납부방법', '납세의무자', '과세표준', '신고납부', '과세표준과 세율',
       '납세의무자, 과세표준 및 세율', '납기', '정의', '세율', '정보']

    for arg in args:
        string = string + "," + '"' + arg + '"' + " VARCHAR(255)"
    query = query + string + ")"


def selectNameFromTable(table,findVar,data):
    conn = getConnection()
    cs = conn.cursor()
    if str(data)[-1] == ' ':
        query = "SELECT * FROM " + table + " WHERE " + findVar + " = " + "'" + data[:-1] + "';"
    elif type(data) == int:
        query = "SELECT * FROM " + table + " WHERE " + findVar + " = " + str(data) + ";"
    else:
        query = "SELECT * FROM " + table + " WHERE " + findVar + " = " + "'" + data + "';"
    print("query : ",query)
    try:
        cs.execute(query)
        all_rows = cs.fetchall()
        return [data for data in all_rows]
    finally:
        conn.close()


def insertDataToTable(question):
    conn = getConnection()
    cs = conn.cursor()
    try:
        query = "INSERT into question_table values (?,?)"
        print("query : ", query)
        cs.execute(query,(0,question))
    finally:
        conn.commit()
        conn.close()


def deleteDataFromTable():
    conn = getConnection()
    cs = conn.cursor()
    try:
        query = "Delete from question_table where id = 0"
        cs.execute(query)
        conn.commit()
    except:
        print("no before_question")
    finally:
        conn.close()



if __name__ == "__main__":
    pass