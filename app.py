import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("WEATHER_API_KEY")

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    try:
        r = requests.get(url)
        return jsonify(r.json())
    except:
        return jsonify({"error": "failed"}), 500

if __name__ == '__main__':
    app.run(port=5000)