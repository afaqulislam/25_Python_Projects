import requests

# ✅ Replace with your actual API key
API_KEY = "eff15a046767461d810143451252301"
API_URL = "https://api.weatherapi.com/v1/current.json"


def get_weather(location):
    try:
        print("\n🔍 Fetching weather...")
        url = f"{API_URL}?key={API_KEY}&q={location}&aqi=yes"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            print(f"❌ Error: {data['error']['message']}")
        else:
            display_weather(data)

    except Exception as e:
        print(f"❌ Failed to fetch weather data: {e}")


def display_weather(data):
    location = data["location"]
    current = data["current"]

    name = location["name"]
    region = location["region"]
    country = location["country"]
    temp_c = current["temp_c"]
    condition = current["condition"]["text"]
    icon = current["condition"]["icon"]

    print(f"\n📍 {name}, {region}, {country}")
    print(f"🌡️  Temperature: {temp_c}°C")
    print(f"🌥️  Condition: {condition}")
    print(f"🖼️  Icon URL: https:{icon}")


if __name__ == "__main__":
    print("=== Monochrome Weather ===")
    location = input("Enter location: ").strip()

    if location:
        get_weather(location)
    else:
        print("⚠️ Please enter a valid location.")
