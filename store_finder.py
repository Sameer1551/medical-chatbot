
import requests
from datetime import datetime
import json

def find_nearby_places(lat=None, lon=None, place_type="pharmacy"):
    """
    Uses OpenStreetMap's Nominatim API to find nearby places
    Includes operating hours and map links
    """
    try:
        # Convert string coordinates to float if needed
        try:
            if lat and lon:
                lat = float(lat)
                lon = float(lon)
        except (ValueError, TypeError):
            print("Invalid coordinates format")
            return []

        if not lat or not lon:
            print("No location coordinates provided")
            return []

        print(f"Searching near coordinates: {lat}, {lon}")
        
        # Using Overpass API for better results
        overpass_url = "https://overpass-api.de/api/interpreter"
        radius = 5000  # 5km radius
        
        # Query for both pharmacies and hospitals
        query = f"""
        [out:json][timeout:25];
        (
          node["amenity"="pharmacy"](around:{radius},{lat},{lon});
          way["amenity"="pharmacy"](around:{radius},{lat},{lon});
          node["amenity"="hospital"](around:{radius},{lat},{lon});
          way["amenity"="hospital"](around:{radius},{lat},{lon});
          node["healthcare"="hospital"](around:{radius},{lat},{lon});
          way["healthcare"="hospital"](around:{radius},{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        """
        
        headers = {
            'User-Agent': 'Medical Store Finder/1.0'
        }
        
        response = requests.post(overpass_url, data=query, headers=headers)
        
        if response.status_code != 200:
            print(f"API request failed with status code: {response.status_code}")
            return []
            
        data = response.json()
        places = []
        
        for element in data.get('elements', [])[:15]:  # Show up to 15 results
            if element.get('type') == 'node':
                tags = element.get('tags', {})
                
                # Basic information
                name = tags.get('name', 'Unnamed Location')
                amenity_type = "Hospital" if tags.get('amenity') == 'hospital' or tags.get('healthcare') == 'hospital' else "Pharmacy"
                
                # Address construction
                address_parts = []
                if tags.get('addr:housenumber'): address_parts.append(tags['addr:housenumber'])
                if tags.get('addr:street'): address_parts.append(tags['addr:street'])
                if tags.get('addr:city'): address_parts.append(tags['addr:city'])
                address = ', '.join(address_parts) if address_parts else 'Address not available'
                
                # Opening hours processing
                opening_hours = tags.get('opening_hours', '24/7' if amenity_type == 'Hospital' else 'Hours not available')
                is_open = "Open 24/7" if opening_hours == '24/7' else "Status unknown"
                
                # Maps URL
                maps_url = f"https://www.google.com/maps?q={element.get('lat')},{element.get('lon')}"
                
                places.append({
                    "name": f"{name} ({amenity_type})",
                    "address": address,
                    "is_open": is_open,
                    "opening_hours": opening_hours,
                    "maps_url": maps_url,
                    "distance": f"{radius/1000:.1f}km radius"
                })
        
        print(f"Found {len(places)} medical facilities")
        return places
        
    except Exception as e:
        print(f"Error finding nearby places: {str(e)}")
        return []
