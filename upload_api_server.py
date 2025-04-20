from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    now = datetime.now().strftime('%Y%m%d-%H%M%S')
    with open(f'uploaded_{now}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
