import os
import requests
import time
import re

print("🚀 AI System Started (Full Upgrade)...")

# ✅ SAHI PATH: Yahan se 'Firent/' hata diya hai
base_dir = "service_url"
os.makedirs(base_dir, exist_ok=True)

token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

# 🔥 MEMORY (Duplicate Rokne ke Liye) 🔥
used_urls = set()

# Pehle se bani files ki memory load karo
if os.path.exists(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith("_url.py"):
                try:
                    with open(os.path.join(root, f), "r") as file:
                        match = re.search(r'requests\.get\("(.*?)"', file.read())
                        if match: used_urls.add(match.group(1))
                except: pass

print(f"📂 Memory mein pehle se {len(used_urls)} URLs hain.")

# A se Z tak loop
for i in range(26):
    letter = chr(65 + i)
    folder_path = os.path.join(base_dir, letter)
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"\n🔄 Processing Folder: {letter} ({i+1}/26)")
        
        # AI ko strict prompt bhej rahe hain
        prompt = f"Give me 1 real JSON API endpoint URL for category '{letter}'. It must be an API, not a documentation website. Format strictly: Category|URL. No extra text."
        url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
        
        res = requests.get(url, timeout=30)
        
        if '|' in res.text:
            parts = res.text.split('|')
            category = parts[0].strip().replace(' ', '_').lower()
            api_url = parts[1].strip()
            
            if api_url.startswith("http"):
                
                # Duplicate Check
                if api_url in used_urls:
                    print(f"⚠️ Duplicate URL found: {api_url}. Skipping...")
                    continue
                
                print(f"🔍 Testing URL: {api_url}")
                
                try:
                    test = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    
                    if test.status_code in [200, 201, 202]:
                        
                        # Check karo ki JSON data de raha hai ya HTML
                        is_json = False
                        try:
                            test.json()
                            is_json = True
                        except: pass
                        
                        if not is_json:
                            print(f"⚠️ URL is HTML page, not API. Skipping...")
                            continue

                        # Details nikalna (Title/Desc)
                        url_title = "No Title"
                        url_desc = "No Description"
                        try:
                            html = test.text
                            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                            if title_match: url_title = title_match.group(1).strip()
                            
                            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
                            if desc_match: url_desc = desc_match.group(1).strip()
                        except: pass
                        
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
                        
                        used_urls.add(api_url)
                        print(f"✅ SUCCESS: Saved to {letter}/{file_name}")
                        
                        # Telegram Message with Details
                        if token and chat_id:
                            msg = f"✅ <b>[{letter}] NEW API URL</b>\n"
                            msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                            msg += f"🔗 <b>URL:</b> <code>{api_url}</code>\n"
                            msg += f"📌 <b>Title:</b> {url_title}\n"
                            msg += f"📝 <b>Desc:</b> {url_desc}\n"
                            msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                            msg += f"📂 <b>Folder:</b> {letter}/{file_name}"
                            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
                    else:
                        print(f"❌ URL Failed (Status {test.status_code}).")
                except Exception as e:
                    print(f"⚠️ Testing Error: {e}")
    except Exception as e:
        print(f"❌ AI Error: {e}")
        
    time.sleep(2)

print("\n🎉 Saare 26 Folders ka Process Complete!")
