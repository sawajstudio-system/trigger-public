import os
import requests

print("🧠 AI System Started: Thinking of new URLs...")

# AI ko strict prompt de rahe hain
prompt = "List 5 real, working open-source API URLs for different categories (like image, weather, crypto, etc.). Format strictly as: Category|URL. Do not add extra text."
url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"

try:
    # Free AI se response lena
    res = requests.get(url, timeout=60)
    ai_response = res.text
    print(f"🤖 AI Response:\n{ai_response}\n")
except Exception as e:
    print(f"❌ AI Network Error: {e}")
    ai_response = ""

base_dir = "Firent/service_url"
os.makedirs(base_dir, exist_ok=True)

used_urls = set()
lines = ai_response.split('\n')
created_count = 0
folder_counter = 0

# Telegram Report banayenge
tg_report = "🧠 <b>[AI SYSTEM REPORT]</b>\n"
tg_report += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

for line in lines:
    if '|' in line:
        parts = line.split('|')
        if len(parts) >= 2:
            category = parts[0].strip().replace(' ', '_').lower()
            api_url = parts[1].strip()
            
            # Agar URL galat format mein hai, toh skip karo
            if not api_url.startswith("http") or api_url in used_urls:
                continue
                
            print(f"🔍 Checking URL: {api_url}")
            
            # 🔥 LIVE CHECK (Police) 🔥
            is_working = False
            status_code = "N/A"
            try:
                test = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                status_code = test.status_code
                if status_code in [200, 201, 202]:
                    is_working = True
            except Exception:
                status_code = "Error"
            
            # Agar URL sahi hai, tabhi file banao
            if is_working:
                used_urls.add(api_url)
                
                # A, B, C folder logic
                letter = chr(65 + (folder_counter % 26))
                folder_path = os.path.join(base_dir, letter)
                os.makedirs(folder_path, exist_ok=True)
                
                # File ka naam (jaise A1_category_url.py)
                file_name = f"{letter}1_{category}_url.py"
                file_path = os.path.join(folder_path, file_name)
                
                code = f"""import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    try:
        res = requests.get("{api_url}", timeout=15)
        send_telegram_message(f"✅ AI Generated ({category}): Status {{res.status_code}}")
    except Exception as e: send_telegram_message(f"❌ Error: {{e}}")
if __name__ == "__main__": run_test()
"""
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                
                print(f"✅ Created: {file_path}")
                tg_report += f"✅ <b>PASSED:</b> {folder_path}/{file_name}\n"
                created_count += 1
                folder_counter += 1
            else:
                tg_report += f"❌ <b>FAILED:</b> {api_url} (Status: {status_code})\n"

tg_report += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
tg_report += f"🎉 <b>Total Real Files Created:</b> {created_count}\n"

# Telegram par report bhejna
token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
if token and chat_id:
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": tg_report, "parse_mode": "HTML"})
        print("✅ Report sent to Telegram!")
    except: pass

print(f"\n🎉 AI System Finished!")
