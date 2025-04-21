from location import get_user_location
from store_finder import find_nearby_places
from ayurveda_helper import load_ayurveda_data, get_ayurveda_tip
from emergency import emergency_call

def chatbot():
    print("🤖 Welcome to the Medical Assistant Chatbot!")

    ayurveda_data = load_ayurveda_data()

    while True:
        user_input = input("You: ").strip().lower()

        if "location" in user_input:
            loc = get_user_location()
            if loc:
                print(f"📍 Your location is approximately: {loc}")
            else:
                print("❌ Unable to get location.")

        elif "medical store" in user_input or "pharmacy" in user_input:
            loc = get_user_location()
            if loc:
                stores = find_nearby_places(loc[0], loc[1])
                print("🩺 Nearby Medical Stores:")
                for store in stores:
                    print(f"• {store['name']} - {store['address']}")
            else:
                print("❌ Cannot fetch nearby stores without location.")

        elif "ayurveda" in user_input or "tip" in user_input:
            issue = input("Enter your health issue (e.g., cough, cold): ")
            print("🌿 Tip:", get_ayurveda_tip(issue, ayurveda_data))

        elif "emergency" in user_input:
            print("📞 Connecting to emergency services...")
            emergency_call()

        elif "exit" in user_input or "quit" in user_input:
            print("👋 Take care! Stay healthy.")
            break

        else:
            print("🤔 I didn't understand that. You can ask about location, medical stores, ayurveda tips, or emergency.")

if __name__ == "__main__":
    chatbot()
