from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

# Load trained model and scaler
model = joblib.load("machine_health_model.pkl")
scaler = joblib.load("scaler.pkl")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get data from form
        data = [
            float(request.form["temperature"]),
            float(request.form["pressure"]),
            float(request.form["vibration"]),
            float(request.form["humidity"]),
            float(request.form["power"]),
            float(request.form["hour"])
        ]

        # Scale and predict
        scaled = scaler.transform([data])
        prob = model.predict_proba(scaled)[0][1]

        # Map probability to health status
        if prob < 0.2:
            status = "good"
        elif prob < 0.5:
            status = "warning"
        else:
            status = "bad"

        return jsonify({"status": status, "probability": round(prob * 100, 2)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
