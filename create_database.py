import sqlite3
from sqlite3 import Error

conn = None

query = """ CREATE TABLE IF NOT EXISTS readings (
                                        reading_id text NOT NULL PRIMARY KEY,
                                        ip text NOT NULL,
                                        data text NOT NULL
                                    ); """
                            
try:
    conn = sqlite3.connect("readings.db")
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(query)
    else:
        print("Error! cannot create the database connection.")

except Error as e:
    print(e)
finally:
    if conn:
        conn.close()
