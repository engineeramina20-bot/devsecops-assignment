from flask import Flask, request, jsonify
import sqlite3
import os
import hashlib
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)

# [span_1](start_span)استخدام متغيرات البيئة بدلاً من السر المكتوب يدوياً[span_1](end_span)
API_KEY = os.getenv("API_KEY", "default-secure-key")

# إعدادات Log آمنة
logging.basicConfig(level=logging.INFO)

@app.route("/auth", methods=["POST"])
def auth():
    username = request.json.get("username")
    password = request.json.get("password")
    
    # [span_2](start_span)تصحيح SQL Injection باستخدام Parameterized Queries[span_2](end_span)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    
    if cursor.fetchone():
        return jsonify({"status": "authenticated"})
    return jsonify({"status": "denied"}), 401

@app.route("/exec", methods=["POST"])
def exec_cmd():
    # [span_3](start_span)منع تنفيذ الأوامر العشوائية - تم استبدالها بوظيفة ثابتة[span_3](end_span)
    return jsonify({"error": "Arbitrary command execution is disabled for security"}), 403

@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.json.get("text", "")
    # [span_4](start_span)استخدام SHA-256 بدلاً من MD5 الضعيف[span_4](end_span)
    hashed = hashlib.sha256(text.encode()).hexdigest()
    return jsonify({"hash": hashed})

@app.route("/file", methods=["POST"])
def read_file():
    filename = request.json.get("filename")
    # [span_5](start_span)منع Path Traversal باستخدام secure_filename[span_5](end_span)
    if filename:
        safe_name = secure_filename(filename)
        # تأكد من وجود الملف في مجلد محدد فقط
        try:
            with open(os.path.join("uploads", safe_name), "r") as f:
                return jsonify({"content": f.read()})
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404
    return jsonify({"error": "Invalid filename"}), 400

@app.route("/debug", methods=["GET"])
def debug():
    # [span_6](start_span)إخفاء المعلومات الحساسة[span_6](end_span)
    return jsonify({"message": "Debug info is restricted in production"})

if __name__ == "__main__":
    # [span_7](start_span)تعطيل debug=True في الإنتاج لمنع تسريب المعلومات[span_7](end_span)
    app.run(host="0.0.0.0", port=5000, debug=False)