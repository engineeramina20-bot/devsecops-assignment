from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os
import logging
import hashlib
from pathlib import Path

app = Flask(__name__)

# Secret via variables d’environnement
API_KEY = os.environ.get("API_KEY")

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent

def get_db():
    return sqlite3.connect(BASE_DIR / "users.db")

@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password").encode()

    conn = get_db()
    cursor = conn.cursor()

    # Requête préparée (anti SQL Injection)
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password, row[0]):
        return jsonify({"status": "authenticated"})
    return jsonify({"status": "denied"}), 401

@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.json.get("text", "")
    # Chiffrement fort
    hashed = hashlib.sha256(text.encode()).hexdigest()
    return jsonify({"hash": hashed})

@app.route("/file", methods=["POST"])
def read_file():
    filename = request.json.get("filename")

    safe_path = BASE_DIR / "files" / os.path.basename(filename)

    if not safe_path.exists():
        return jsonify({"error": "File not found"}), 404

    with open(safe_path, "r") as f:
        return jsonify({"content": f.read()})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/log", methods=["POST"])
def log_data():
    data = request.json
    logging.info("User action received")
    return jsonify({"status": "logged"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)