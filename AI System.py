import os
import requests
import time
import re

print("🚀 Real Data System Started (No AI, 100% Working)...")

base_dir = "service_url"
os.makedirs(base_dir, exist_ok=True)

token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

# 🔥 100% REAL, WORKING URLs KI MASTER LIST 🔥
real_platforms = [
    ("A", "A1_image_url.py", "https://image.pollinations.ai/prompt/cyberpunk", "AI Image Generator"),
    ("B", "B1_weather_url.py", "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true", "Weather API"),
    ("C", "C1_books_url.py", "https://openlibrary.org/search.json?q=python", "Books Search API"),
    ("D", "D1_crypto_url.py", "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", "Crypto Prices API"),
    ("E", "E1_countries_url.py", "https://restcountries.com/v3.1/all", "Countries Info API"),
    ("F", "F1_jokes_url.py", "https://official-joke-api.appspot.com/random_joke", "Jokes API"),
    ("G", "G1_quotes_url.py", "https://zenquotes.io/api/random", "Quotes API"),
    ("H", "H1_nasa_url.py", "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", "NASA Space API"),
    ("I", "I1_ip_url.py", "https://api.ipify.org?format=json", "IP Address API"),
    ("J", "J1_pokemon_url.py", "https://pokeapi.co/api/v2/pokemon/pikachu", "Pokemon API"),
    ("K", "K1_anime_url.py", "https://api.jikan.moe/v4/anime/1", "Anime API"),
    ("L", "L1_food_url.py", "https://www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata", "Food Recipe API"),
    ("M", "M1_currency_url.py", "https://open.er-api.com/v6/latest/USD", "Currency Exchange API"),
    ("N", "N1_dictionary_url.py", "https://api.dictionaryapi.dev/api/v2/entries/en/hello", "Dictionary API"),
    ("O", "O1_github_url.py", "https://api.github.com/users/octocat", "GitHub User API"),
    ("P", "P1_rickmorty_url.py", "https://rickandmortyapi.com/api/character/1", "Rick & Morty API"),
    ("Q", "Q1_harrypotter_url.py", "https://hp-api.onrender.com/api/characters", "Harry Potter API"),
    ("R", "R1_catfact_url.py", "https://catfact.ninja/fact", "Cat Facts API"),
    ("S", "S1_quran_url.py", "https://api.alquran.cloud/v1/ayah/2:255/edition/quran-uthmani", "Quran API"),
    ("T", "T1_hadith_url.py", "https://random-hadith-generator.vercel.app/bukhari/", "Hadith API"),
    ("U", "U1_quote2_url.py", "https://api.quotable.io/random", "Quotable API"),
    ("V", "V1_bored_url.py", "https://www.boredapi.com/api/activity", "Bored Activity API"),
    ("W", "W1_age_url.py", "https://api.agify.io?name=meelad", "Age Predictor API"),
    ("X", "X1_gender_url.py", "https://api.genderize.io?name=lucy", "Gender Predictor API"),
    ("Y", "Y1_nationalize_url.py", "https://api.nationalize.io?name=nathaniel", "Nationality Predictor API"),
    ("Z", "Z1_breakingbad_url.py", "https://www.breakingbadapi.com/api/characters/1", "Breaking Bad API")
]

for letter, file_name, api_url, desc in real_platforms:
    folder_path = os.path.join(base_dir, letter)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    
    print(f"\n🔄 Processing [{letter}]: {desc}")
    
    try:
        test = requests.get(api_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        
        if test.status_code in [200, 201, 202]:
            # Code file likhna
            code = f"""import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("{api_url}", timeout=15)
        send_telegram_message(f"✅ Verified ({desc}): Status {{res.status_code}}")
    except Exception as e: send_telegram_message(f"❌ Error: {{e}}")
if __name__ == "__main__": run_test()
"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            print(f"✅ SUCCESS: Saved to {letter}/{file_name}")
            
            # Telegram Message
            if token and chat_id:
                msg = f"✅ <b>[{letter}] REAL API URL</b>\n"
                msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                msg += f"🔗 <b>URL:</b> <code>{api_url}</code>\n"
                msg += f"📝 <b>Kaam:</b> {desc}\n"
                msg += f"📊 <b>Status:</b> {test.status_code}\n"
                msg += f"📂 <b>Folder:</b> {letter}/{file_name}"
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
        else:
            print(f"❌ FAILED: Status {test.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
    time.sleep(1)

print("\n🎉 Saare 26 Real URLs process ho gaye!")
