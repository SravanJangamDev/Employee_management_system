import sqlite3
import falcon

query_users = """create table users (
		id INTEGER NOT NULL PRIMARY KEY autoincrement, 
		username TEXT NOT NULL, 
		password TEXT NOT NULL, 
		token TEXT NULL, 
		token_time INTEGER NULL,
		salt TEXT NULL 
	)"""

query_employees = """create table employees (
		id INTEGER NOT NULL PRIMARY KEY autoincrement, 
		name TEXT NOT NULL, 
		salary INTEGER NULL, 
		address TEXT NULL, 
		designation TEXT NULL 
	)"""


def mysql_action(query, msg):
    try:
        connection = sqlite3.connect("test.db")
        cur = connection.cursor()
        cur.execute(query)
        data = []
        for user in cur:
            data.append(user)
        connection.commit()
        connection.close()
        return data
    except Exception as e:
        print("sql error ", e)
        raise falcon.HTTPUnauthorized(
            title="Internal server error", description=msg + " failed"
        )
