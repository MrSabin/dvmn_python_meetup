import json
import sqlite3


def db_to_json(query):
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(query)
    json_string = json.dumps(cursor.fetchall(), ensure_ascii=False)
    db.close()
    return json_string
