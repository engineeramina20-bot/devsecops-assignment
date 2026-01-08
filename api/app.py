from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    
    user = cursor.fetchone()
    if user:
        return jsonify({"message": "Success"})
    return jsonify({"message": "Failed"}), 401

@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.json.get("text", "")
    hashed = hashlib.sha256(text.encode()).hexdigest()
    return jsonify({"hash": hashed})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)