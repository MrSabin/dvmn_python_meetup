import json
import sqlite3

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()
cursor.execute("SELECT * FROM bot_db_speaker")
json_string = json.dumps(cursor.fetchall())
print(json_string)

db.close()
