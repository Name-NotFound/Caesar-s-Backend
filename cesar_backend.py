from flask import Flask, request, jsonify
from datetime import date
import sqlite3


app = Flask(__name__)
conn = sqlite3.connect('../requests.db', check_same_thread=False)
cur = conn.cursor()

if __name__ == '__main__':
    def encrypt2caesar(rot, word):

        return ''.join([chr((ord(let) + rot - 97) % 26 + 97) if ord(let) in range(97, 123) else let for let in word])


    @app.route('/encode', methods=['POST'])
    def encode():
        content = request.json
        cur.execute("INSERT INTO requests VALUES(?, ?);", (date.today(), content['rot']))
        conn.commit()

        return jsonify({"message": encrypt2caesar(content['rot'], content['message'])})


    @app.route('/decode/message=<string:message>&rot=<int:rot>', methods=['GET'])
    def decode(message, rot):

        return jsonify({"message": encrypt2caesar(-rot, message)})


    @app.route('/stats', methods=['GET'])
    def stats():
        cur.execute(f"SELECT rot, count(*) FROM requests WHERE date = '{date.today()}' GROUP BY rot")

        return jsonify(sorted([{"rot": elem[0], "usages": elem[1]} for elem in cur.fetchall()], key=lambda d: d['rot']))


    app.run(host= '0.0.0.0',debug=True)
