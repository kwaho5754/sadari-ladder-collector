from flask import Flask, render_template_string
import predictor  # predictor.py의 get_prediction_list() 함수 사용
import pandas as pd
import os

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)