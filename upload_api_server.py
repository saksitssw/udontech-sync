from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# -------------------------------
# หน้าหลัก "/" ใช้เช็คสถานะ API
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "✅ UdonTech API is running.",
        "upload_endpoint": "/api/upload",
        "status": "OK"
    })

# -------------------------------
# API รับข้อมูลหลักสูตร / ข่าว / โพสต์ ฯลฯ
@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    now = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f'uploaded_{now}.json'

    # สร้างโฟลเดอร์เก็บข้อมูลถ้ายังไม่มี
    os.makedirs("data_uploads", exist_ok=True)

    # เขียนไฟล์ลงโฟลเดอร์
    with open(os.path.join("data_uploads", filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return jsonify({"status": "success", "saved_as": filename})

# -------------------------------
# Run Flask บน PORT จาก Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render กำหนด PORT ผ่าน env
    app.run(host='0.0.0.0', port=port)
