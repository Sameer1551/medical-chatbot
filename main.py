
from flask import Flask, render_template, request, jsonify
from location import get_user_location
from store_finder import find_nearby_places
from ayurveda_helper import load_ayurveda_data, get_ayurveda_tip
from emergency import emergency_call

app = Flask(__name__)
ayurveda_data = load_ayurveda_data()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip().lower()
    
    if "location" in user_input:
        loc = get_user_location()
        if loc:
            coords = loc['coordinates']
            place = loc['place_name']
            return jsonify({"response": f"📍 Your location is: {place}\nCoordinates: {coords[0]}, {coords[1]}"})
        return jsonify({"response": "❌ Unable to get location."})

    elif "medical store" in user_input or "pharmacy" in user_input or "hospital" in user_input:
        # Try to get location from request
        lat = request.args.get('latitude')
        lon = request.args.get('longitude')
        
        if not (lat and lon):
            # Try to get location from user location service
            loc = get_user_location()
            if loc:
                lat, lon = loc[0], loc[1]
            else:
                return jsonify({
                    "response": "📍 Please share your location to find nearby medical facilities.",
                    "request_location": True
                })
        
        print(f"Location received: {lat}, {lon}")  # Debug print
        stores = find_nearby_places(lat=lat, lon=lon)
        if not stores:
            return jsonify({"response": "❌ No medical facilities found in your area. Try increasing the search radius."})
            
        response = "🏥 Nearby Medical Facilities:\n"
        for store in stores:
            response += f"• {store['name']}\n"
            response += f"  📍 {store['address']}\n"
            response += f"  ⏰ {store['is_open']}\n"
            if store['opening_hours'] != 'Hours not available':
                response += f"  📅 {store['opening_hours']}\n"
            response += f"  🗺️ [Open in Maps]({store['maps_url']})\n\n"
        return jsonify({"response": response})

    elif "ayurveda" in user_input or "tip" in user_input:
        return jsonify({"response": "Please enter your health issue:", "prompt": True})

    elif "issue:" in user_input:
        issue = user_input.replace("issue:", "").strip()
        tip = get_ayurveda_tip(issue, ayurveda_data)
        return jsonify({"response": f"🌿 Tip: {tip}"})

    elif "emergency" in user_input:
        emergency_call()
        return jsonify({"response": "📞 Connected to emergency services..."})

    else:
        return jsonify({"response": "🤔 I didn't understand that. You can ask about location, medical stores, ayurveda tips, or emergency."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
