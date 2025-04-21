
from flask import request, jsonify
import requests
import time

def get_place_name(lat, lon):
    """Get place name from coordinates using Nominatim API"""
    try:
        # Add delay to respect Nominatim usage policy
        time.sleep(1)
        
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        headers = {
            'User-Agent': 'MedicalHelper/1.0'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Get display name which includes full address
            return data.get('display_name', 'Location name not found')
        return None
    except Exception as e:
        print(f"Error getting place name: {str(e)}")
        return None

def get_user_location():
    # Try to get coordinates from query parameters first
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    
    # If not in query params, try request body
    if not (lat and lon):
        data = request.get_json()
        if data and 'coords' in data:
            lat = data['coords'].get('latitude')
            lon = data['coords'].get('longitude')
    
    if lat and lon:
        try:
            lat_float = float(lat)
            lon_float = float(lon)
            place_name = get_place_name(lat_float, lon_float)
            return {
                'coordinates': [lat_float, lon_float],
                'place_name': place_name
            }
        except (ValueError, TypeError):
            return None
    return None
