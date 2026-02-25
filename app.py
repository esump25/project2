import google.generativeai as genai
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

# AI Configuration
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
print("--- DEBUG: LISTING MODELS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"AVAILABLE MODEL: {m.name}")
except Exception as e:
    print(f"COULD NOT LIST MODELS: {e}")
print("--- END DEBUG ---")
model = genai.GenerativeModel('gemini-2.0-flash-lite')

API_KEY = os.getenv("WEATHER_API_KEY")

@app.route('/')
def home():
    return "Server is up!"

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    try:
        r = requests.get(url)
        return jsonify(r.json())
    except:
        return jsonify({"error": "failed"}), 500

# NEW: AI Itinerary Route
@app.route('/api/itinerary', methods=['GET'])
def get_itinerary():
    # Catching all the specific user answers from the frontend request
    city = request.args.get('city')
    budget = request.args.get('budget')
    activity = request.args.get('activity')
    duration = request.args.get('duration')
    traveler = request.args.get('traveler')
    cuisine = request.args.get('cuisine')
    pace = request.args.get('pace')
    
    # Constructing a highly tailored prompt
    prompt = (
    f"Act as a professional travel guide. Task: Create a concise travel itinerary for {city}. "
    f"Traveler Profile: {traveler}. Duration: {duration}. Budget: {budget}. "
    f"Focus: {activity}. Pace: {pace}. Dining: {cuisine}. "
    f"Output Structure: Use 'Day X' headings followed by 3-4 simple bullet points per day. "
    f"Style: Plain text only. No bolding. No introduction. No conclusion. "
    f"Limit: Maximum 250 words."
    )
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"itinerary": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)