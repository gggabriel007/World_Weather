import requests
from dotenv import load_dotenv
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_emoji(condition):
    condition = condition.lower()
    if "sunny" in condition or "clear" in condition:
        return "☀️"
    elif "cloud" in condition or "overcast" in condition:
        return "☁️"
    elif "rain" in condition or "shower" in condition:
        return "🌧️"
    elif "snow" in condition:
        return "❄️"
    elif "thunder" in condition:
        return "⛈️"
    elif "mist" in condition or "fog" in condition or "haze" in condition:
        return "🌫️"
    else:
        return "🌡️"

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        print(f"❌ {data['error']['message']} for {city}")
        return None

    location = data['location']['name']
    country = data['location']['country']
    localtime = data['location']['localtime']

    print(f"\n--- 3-Day Forecast for {location}, {country} ---")
    print(f"Local Time: {localtime}")

    max_temps = []
    for day in data['forecast']['forecastday']:
        date = day['date']
        max_temp = day['day']['maxtemp_c']
        min_temp = day['day']['mintemp_c']
        condition = day['day']['condition']['text']
        emoji = get_emoji(condition)

        print(f"{date}: {emoji} {condition} | High: \033[91m{max_temp}C\033[0m | Low: \033[94m{min_temp}C\033[0m")

        with open("weather_log.txt", "a", encoding="utf-8") as file:
            file.write(f"{date} | {location}, {country} | {condition} | High: {max_temp}C | Low: {min_temp}C\n")
        
        max_temps.append(max_temp)

    return {"city": f"{location}, {country}", "high": max(max_temps) if max_temps else 0}

def main():
    all_cities = []
    while True:
        cities_input = input("\nEnter city names separated by commas, or type 'quit' to exit: ")
        if cities_input.lower() == 'quit':
            break

        city_list = [c.strip() for c in cities_input.split(",") if c.strip()]

        for CITY in city_list:
            try:
                print(f"\nFetching 3-Day Weather for {CITY}...")
                city_data = get_weather(CITY)
                if city_data:
                    all_cities.append(city_data)
            except Exception as e:
                print(f"❌ City '{CITY}' not found. Error: {e}")

        print("Saved to weather_log.txt")

        if all_cities:
            hottest = max(all_cities, key=lambda x: x['high'])
            coldest = min(all_cities, key=lambda x: x['high'])
            print(f"\n🌍 GLOBAL SUMMARY: Hottest: {hottest['city']} \033[91m{hottest['high']}C\033[0m | Coldest: {coldest['city']} \033[94m{coldest['high']}C\033[0m")

if __name__ == "__main__":
    main()