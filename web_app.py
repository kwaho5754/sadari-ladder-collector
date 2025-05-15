from flask import Flask, render_template_string
import predictor  # predictor.py의 predict() 함수 사용

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

if __name__ == "__main__":
    app.run(debug=True)
