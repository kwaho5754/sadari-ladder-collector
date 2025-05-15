from flask import Flask, render_template_string
import predictor
import pandas as pd
import os
import threading
import time
import collect_ladder  # 수집기 임포트

app = Flask(__name__)

@app.route("/predict")
def predict_route():
    data = predictor.get_prediction_list()
    html = """
    <h2>🔮 사다리 예측 결과 (Top 3)</h2>
    <ol>
        {% for rank, direction, count in data %}
            <li>{{ rank }}위: {{ direction }} (출현: {{ count }}회)</li>
        {% endfor %}
    </ol>
    """
    return render_template_string(html, data=data)

@app.route("/count")
def count_csv_rows():
    csv_path = "ladder_results.csv"
    if not os.path.exists(csv_path):
        return "❌ ladder_results.csv 파일이 존재하지 않습니다."
    try:
        df = pd.read_csv(csv_path)
        return f"✅ 현재 누적 회차 수: {len(df)}개"
    except Exception as e:
        return f"⚠️ 오류 발생: {str(e)}"

# 🔁 수집기 실행 (백그라운드 스레드)
def run_collector():
    while True:
        try:
            collect_ladder.wait_for_next_result()
        except Exception as e:
            print(f"❌ 수집기 오류 발생: {e}")
        print("⏱️ 다음 5분까지 대기...\n")
        time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=run_collector, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
