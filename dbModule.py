import sqlite3 as lite


def getConnection():
    db_name = "minwon.db"
    return lite.connect(db_name)


def getCursor(conn):
    return conn.cursor()


def selectAllFromTableUsingWhere(table,findVar,data):
    """
    select All Values From DB Table Using Where clause
    :param table: DB table name, type: String
    :param findVar: want to find column name, type: String
    :param data: value to find in column, type: String
    :return:
    """
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


def selectThingFromTableUsingWhere(select,table,where,data):
    """
    select value from table using where clause
    :param select: value to find select clause type:String
    :param table: DB table name, type: String
    :param where: the name that want to find in column
    :param data:
    :return:
    """
    conn = getConnection()
    cs = conn.cursor()
    if str(data)[-1] == ' ':
        query = "SELECT " + select + " FROM " + table + " WHERE " + where + " = " + "'" + data[:-1] + "';"
    elif type(data) == int:
        query = "SELECT " + select + " FROM " + table + " WHERE " + where + " = " + str(data) + ";"
    else:
        query = "SELECT " + select + " FROM " + table + " WHERE " + where + " = " + "'" + data + "';"
    print("query : ", query)

    try:
        cs.execute(query)
        all_rows = cs.fetchall()
        return [data for data in all_rows]
    finally:
        conn.close()


def selectThingFromTable(select,table):
    """
    select value from table
    :param select: value to find in Table, type: String
    :param table: DB table name,type: String
    :return: all data which user wanted type: list
    """
    conn = getConnection()
    cs = conn.cursor()

    query = "SELECT " + select + " FROM " + table + " ;"
    print("query : ", query)

    try:
        cs.execute(query)
        all_rows = cs.fetchall()
        return [data for data in all_rows]
    finally:
        conn.close()


def insertDataToTable(question):
    """
    Insert value in Database
    :param question: data type: String
    """
    conn = getConnection()
    cs = conn.cursor()
    query = "INSERT into question_table values (?,?)"
    print("query : ", query)

    try:
        cs.execute(query,(0,question))
    finally:
        conn.commit()
        conn.close()


def deleteDataFromTable():
    """
    Delete Data From Table
    """
    conn = getConnection()
    cs = conn.cursor()
    query = "Delete from question_table where id = 0"
    try:
        cs.execute(query)
        conn.commit()
    except:
        print("no before_question")
    finally:
        conn.close()


def getColumnName():
    """
    get table info
    :return: all table info type: Tuple
    """
    conn = getConnection()
    cs = conn.cursor()

    query = "pragma table_info(minwon_info)"
    print("query : ", query)

    try:
        cs.execute(query)
        all_rows = cs.fetchall()
        return [data for data in all_rows]
    finally:
        conn.close()


if __name__ == "__main__":
    pass