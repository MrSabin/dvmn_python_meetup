import json
import sqlite3


def db_to_json(sql_query):
    answer = []
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(sql_query)
    json_string = json.dumps(cursor.fetchall(), ensure_ascii=False)
    db.close()
    formatted = json.loads(json_string)
    for entry in formatted:
        answer.append(entry[0])
    return answer
