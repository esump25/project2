import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai  # <--- Updated to the new 2026 SDK

load_dotenv()
app = Flask(__name__)
CORS(app)

# 1. New Client Initialization (Pick up API key from env)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Heartbeat route to prevent Render 404 health-check failures
@app.route('/')
def home():
    return "Travel Backend is Live!"

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    API_KEY = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    try:
        r = requests.get(url)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/itinerary', methods=['GET'])
def get_itinerary():
    city = request.args.get('city')
    budget = request.args.get('budget')
    activity = request.args.get('activity')
    duration = request.args.get('duration')
    traveler = request.args.get('traveler')
    cuisine = request.args.get('cuisine')
    pace = request.args.get('pace')
    
    # 3. Optimized Prompt for 2026 Speed (under 250 words)
    prompt = (
        f"Professional travel guide mode. Task: Create a concise travel itinerary for {city}. "
        f"Profile: {traveler}, {duration}, {budget} budget. "
        f"Agenda: {activity}. Pace: {pace}. Cuisine: {cuisine}. "
        f"Instructions: Start directly with 'Day 1'. Use bullet points only. "
        f"Style: Plain text. No bolding (**). No intro or outro. "
        f"Constraint: Maximum 250 words total."
    )
    
    try:
        # 4. Using the faster 2026 generation method
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=prompt
        )
        return jsonify({"itinerary": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "The AI is taking a siesta. Try a shorter duration!"}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)