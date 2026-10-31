import os
import requests
import time

print("🚀 AI Auto-Pilot: Looping 26 times to add new URLs...")

base_dir = "service_url"
os.makedirs(base_dir, exist_ok=True)

# Telegram Report
tg_report = "🤖 <b>[AI AUTO-PILOT - 26 URL CYCLE]</b>\n"
tg_report += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

# 26 baar loop chalega (A se Z)
for i in range(26):
    letter = chr(65 + i) # A, B, C... Z
    folder_path = os.path.join(base_dir, letter)
    os.makedirs(folder_path, exist_ok=True)
    
    print(f"\n🔄 Processing Folder: {letter} ({i+1}/26)")
    
    # AI se naya URL mangwa rahe hain
    prompt = f"Give me 1 real, working open-source API URL for category '{letter}'. Format strictly: Category|URL. No extra text."
    url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
    
    try:
        res = requests.get(url, timeout=60)
        ai_response = res.text
        
        if '|' in ai_response:
            parts = ai_response.split('|')
            category = parts[0].strip().replace(' ', '_').lower()
            api_url = parts[1].strip()
            
            if api_url.startswith("http"):
                print(f"🔍 Testing URL: {api_url}")
                try:
                    test = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    if test.status_code in [200, 201, 202]:
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
                        tg_report += f"✅ <b>[{letter}] PASSED:</b> {category}\n  🔗 <code>{api_url}</code>\n\n"
                    else:
                        print(f"❌ FAILED: Status {test.status_code}")
                        tg_report += f"❌ <b>[{letter}] FAILED:</b> Status {test.status_code}\n\n"
                except Exception as e:
                    print(f"❌ NETWORK ERROR: {e}")
                    tg_report += f"❌ <b>[{letter}] ERROR:</b> Network\n\n"
    except Exception as e:
        print(f"❌ AI Error: {e}")
    
    time.sleep(2) # 2 second ruko

tg_report += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
tg_report += f"🎉 <b>26 URL Cycle Complete!</b>\n"

# Telegram par Report bhejna
token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

if token and chat_id:
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": tg_report, "parse_mode": "HTML"})
        print("✅ Report sent to Telegram!")
    except:
        print("❌ Report send failed.")

print("\n🎉 26 URLs Process Complete! Run again manually to add more.")
