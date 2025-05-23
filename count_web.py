from flask import Flask
import pandas as pd
import os

app = Flask(__name__)

@app.route("/count")
def count_csv_rows():
    csv_path = "ladder_results.csv"
    if not os.path.exists(csv_path):
        return "❌ ladder_results.csv 파일이 존재하지 않습니다."
    try:
        df = pd.read_csv(csv_path)
        return f"✅ 현재 누적 회차 수: {len(df)}개"
    except Exception as e:
        return f"⚠️ CSV 열기 실패: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
