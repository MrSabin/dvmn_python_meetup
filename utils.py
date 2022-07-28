import json
import sqlite3


def db_to_json():
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bot_db_speaker")
    json_string = json.dumps(cursor.fetchall())
    db.close()
    return json_string
