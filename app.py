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
model = genai.GenerativeModel('gemini-1.5-flash')

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
        f"Act as a professional travel guide. Create a custom itinerary for {city}. "
        f"The traveler is a {traveler} looking for a {duration} trip with a {budget} budget. "
        f"Their main agenda is {activity} and they want a daily pace that is {pace}. "
        f"Make sure to recommend specific dining spots for {cuisine} food. "
        f"Keep the formatting clean: use 'Day X' headings and short bullet points. "
        f"Do not use markdown bolding (**)."
    )
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"itinerary": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "AI could not generate itinerary"}), 500

if __name__ == '__main__':
    # Use 0.0.0.0 for Render deployment
    app.run(host='0.0.0.0', port=5000)