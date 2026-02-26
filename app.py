import google.generativeai as genai
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

# 1. Direct configuration is safer for Cloud
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/')
def home():
    return "Server is live!"

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    # 2. Pull key inside the route for reliability
    w_key = os.environ.get("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={w_key}"
    try:
        r = requests.get(url, timeout=10) # Added timeout so it doesn't hang
        return jsonify(r.json())
    except:
        return jsonify({"error": "failed"}), 500

@app.route('/api/itinerary', methods=['GET'])
def get_itinerary():
    city = request.args.get('city')
    budget = request.args.get('budget') 
    activity = request.args.get('activity')
    duration = request.args.get('duration')
    traveler = request.args.get('traveler')
    cuisine = request.args.get('cuisine')
    pace = request.args.get('pace')
    
    # 3. Short prompt = Fast response = No Timeout
    prompt = (
        f"Create a travel itinerary for {city}. "
        f"Trip Details: {duration} trip, {budget} budget, {traveler} style. "
        f"Focus: {activity} and {cuisine} food. Pace: {pace}. "
        f"Format: Day X headings with 3 short bullet points. "
        f"Style: Plain text. No bolding. No intro. Max 200 words."
    )
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"itinerary": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "AI taking too long, try again"}), 500

if __name__ == '__main__':
    # This line is the 'Secret Sauce' for Render
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host='0.0.0.0', port=port)