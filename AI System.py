import os
import requests
import time
import re

print("🚀 AI System Started (Error-Free Version)...")

# ✅ Sahi Path (Bina Firent/ ke)
base_dir = "service_url"
os.makedirs(base_dir, exist_ok=True)

token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

# A se Z tak loop
for i in range(26):
    letter = chr(65 + i) # A, B, C... Z
    folder_path = os.path.join(base_dir, letter)
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"\n🔄 Processing Folder: {letter} ({i+1}/26)")
        
        prompt = f"Give me 1 real, working open-source API URL for '{letter}'. Format strictly: Category|URL. No extra text."
        url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
        
        # AI se URL mangwana
        res = requests.get(url, timeout=30)
        ai_response = res.text
        
        if '|' in ai_response:
            parts = ai_response.split('|')
            category = parts[0].strip().replace(' ', '_').lower()
            api_url = parts[1].strip()
            
            if api_url.startswith("http"):
                print(f"🔍 Testing URL: {api_url}")
                
                # LIVE CHECK (Yahan error aane par script nahi rukegi)
                try:
                    test = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    
                    if test.status_code in [200, 201, 202]:
                        # URL Details
                        url_title = "No Title"
                        url_desc = "No Description"
                        try:
                            html = test.text
                            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                            if title_match: url_title = title_match.group(1).strip()
                            
                            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
                            if not desc_match:
                                desc_match = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
                            if desc_match: url_desc = desc_match.group(1).strip()
                        except:
                            pass
                        
                        # File Banao
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
                        
                        print(f"✅ SUCCESS: Saved to {letter}/{file_name}")
                        
                        # 1 URL = 1 Telegram Message
                        if token and chat_id:
                            msg = f"✅ <b>[{letter}] NEW URL ADDED</b>\n"
                            msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                            msg += f"🔗 <b>URL:</b> <code>{api_url}</code>\n"
                            msg += f"📌 <b>Title:</b> {url_title}\n"
                            msg += f"📝 <b>Description:</b> {url_desc}\n"
                            msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                            msg += f"📂 <b>Saved in:</b> <code>{letter}/{file_name}</code>\n"
                            msg += f"📊 <b>Status:</b> {test.status_code}"
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
        # Agar AI se hi response na aaye, toh bhi loop rukega nahi
        print(f"❌ AI Network Error: {e}. Moving to next folder...")
        
    # 2 second ruko (Telegram rate limit se bachne ke liye)
    time.sleep(2)

print("\n🎉 Saare 26 Folders ka Process Complete! Run again manually to add more.")
