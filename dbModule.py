import sqlite3 as lite

categories = ['과세대상', '납부방법', '납세의무자', '과세표준', '신고납부', '과세표준과 세율',
       '납세의무자, 과세표준 및 세율', '납기', '정의', '세율', '정보']
def get_Cursor():
    db_name = "minwon.db"
    return lite.connect(db_name).cursor()

def create_table():
    query = "CREATE TABLE IF NOT EXISTS minwon_infomation (id INTEGER PRIMARY_KEY NOT NULL, " \
            "name VARCHAR(255)"
    string =''
    args = ['과세대상', '납부방법', '납세의무자', '과세표준', '신고납부', '과세표준과 세율',
       '납세의무자, 과세표준 및 세율', '납기', '정의', '세율', '정보']


    for arg in args:
        string = string + "," + '"' + arg + '"' + " VARCHAR(255)"
    query = query + string + ")"

def selectNameFromTable(name):
    conn = get_Cursor()
    query = "SELECT * FROM minwon_infomation WHERE name = " + "'"+ name + "';"
    try:
        conn.execute(query)
        all_rows = conn.fetchall()

        return [data for data in all_rows]
    finally:
        conn.close()


if __name__ == "__main__":
    pass