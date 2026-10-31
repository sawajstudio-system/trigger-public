import os
import requests
import time
import re

print("🚀 AI System Started (With Duplicate Checker)...")

# ✅ Sahi Path
base_dir = "service_url"
os.makedirs(base_dir, exist_ok=True)

token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

# 🔥 YEH HAI URL KI MEMORY (Duplicate rokne ke liye) 🔥
used_urls = set()

# Agar pehle se koi file hai, toh uske URLs memory mein daal do
if os.path.exists(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith("_url.py"):
                try:
                    with open(os.path.join(root, f), "r") as file:
                        content = file.read()
                        # File ke andar se URL nikalna
                        match = re.search(r'requests\.get\("(.*?)"', content)
                        if match:
                            used_urls.add(match.group(1))
                except:
                    pass

print(f"📂 Pehle se {len(used_urls)} URLs memory mein hain.")

# A se Z tak loop
for i in range(26):
    letter = chr(65 + i) # A, B, C... Z
    folder_path = os.path.join(base_dir, letter)
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"\n🔄 Processing Folder: {letter} ({i+1}/26)")
        
        # AI ko strict prompt bhej rahe hain (JSON API maang rahe hain)
        prompt = f"Give me 1 real JSON API endpoint URL for '{letter}'. It must be an API, not a documentation website. Format strictly: Category|URL. No extra text."
        url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
        
        res = requests.get(url, timeout=30)
        ai_response = res.text
        
        if '|' in ai_response:
            parts = ai_response.split('|')
            category = parts[0].strip().replace(' ', '_').lower()
            api_url = parts[1].strip()
            
            if api_url.startswith("http"):
                
                # 🔥 DUPLICATE CHECK 🔥
                if api_url in used_urls:
                    print(f"⚠️ Duplicate URL found: {api_url}. Skipping...")
                    continue
                
                print(f"🔍 Testing URL: {api_url}")
                
                try:
                    test = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    
                    if test.status_code in [200, 201, 202]:
                        
                        # Check karo ki yeh JSON data de raha hai ya HTML page
                        is_json = False
                        try:
                            test.json() # Agar JSON hai toh error nahi aayega
                            is_json = True
                        except:
                            pass
                            
                        if not is_json:
                            print(f"⚠️ URL is HTML page, not API: {api_url}. Skipping...")
                            continue

                        url_title = "JSON API Data"
                        url_desc = "Valid API Endpoint"
                        
                        file_name = f"{letter}1_{category}_url.py"
                        file_path = os.path.join(folder_path, file_name)
                        
                        code = f"""import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("{api_url}", timeout=15)
        send_telegram_message(f"✅ AI Verified ({category}): Status {{res.status_code}}")
    except Exception as e: send_telegram_message(f"❌ Error: {{e}}")
if __name__ == "__main__": run_test()
"""
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(code)
                        
                        # Memory mein daal do
                        used_urls.add(api_url)
                        
                        print(f"✅ SUCCESS: Saved to {letter}/{file_name}")
                        
                        if token and chat_id:
                            msg = f"✅ <b>[{letter}] NEW API URL</b>\n"
                            msg += f"🔗 <code>{api_url}</code>"
                            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
                            
                    else:
                        print(f"❌ URL Failed (Status {test.status_code}). Moving to next...")
                        
                except Exception as e:
                    print(f"⚠️ Testing Error: {e}. Moving to next...")
            else:
                print("⚠️ AI gave invalid URL format. Moving to next...")
        else:
            print("⚠️ AI response was not in correct format. Moving to next...")
            
    except Exception as e:
        print(f"❌ AI Network Error: {e}. Moving to next folder...")
        
    time.sleep(2)

print("\n🎉 Saare 26 Folders ka Process Complete!")
