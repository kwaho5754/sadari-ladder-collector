# ✅ server_web.py (서버에 저장된 ladder_results.csv 줄 수 확인용)
from flask import Flask
import csv
import os

app = Flask(__name__)

@app.route("/count")
def count_ladder_rows():
    filename = "ladder_results.csv"
    if not os.path.exists(filename):
        return "❌ ladder_results.csv 파일이 존재하지 않습니다."

    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            return f"✅ 현재까지 저장된 회차 수: {len(rows)-1} 개"  # 헤더 제외
    except Exception as e:
        return f"⚠️ 오류 발생: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
