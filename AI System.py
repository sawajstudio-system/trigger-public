import os
import requests
import time
import re

print("🚀 AI System Started (With Details & Smart AI Check)...")

base_dir = "service_url"
os.makedirs(base_dir, exist_ok=True)

token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

used_urls = set()

# Pehle se bani files ki memory
if os.path.exists(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith("_url.py"):
                try:
                    with open(os.path.join(root, f), "r") as file:
                        match = re.search(r'requests\.get\("(.*?)"', file.read())
                        if match: used_urls.add(match.group(1))
                except: pass

for i in range(26):
    letter = chr(65 + i)
    folder_path = os.path.join(base_dir, letter)
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"\n🔄 Processing Folder: {letter}")
        
        prompt = f"Give me 1 real JSON API URL for '{letter}'. Not a website. Format: Category|URL."
        url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
        
        res = requests.get(url, timeout=30)
        
        if '|' in res.text:
            parts = res.text.split('|')
            category = parts[0].strip().replace(' ', '_').lower()
            api_url = parts[1].strip()
            
            if api_url.startswith("http") and api_url not in used_urls:
                print(f"🔍 Testing URL: {api_url}")
                
                try:
                    test = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    
                    if test.status_code in [200, 201, 202]:
                        # 🔥 YAHAN DETAILS NIKAL RAHE HAIN 🔥
                        url_title = ""
                        url_desc = ""
                        
                        try:
                            html = test.text
                            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                            if title_match: url_title = title_match.group(1).strip()
                            
                            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
                            if desc_match: url_desc = desc_match.group(1).strip()
                        except: pass
                        
                        # Agar details nahi mili, toh AI se poochho ki yeh kya hai
                        if not url_title or not url_desc:
                            print("🤖 Asking AI what this URL does...")
                            ask_ai_url = f"https://text.pollinations.ai/What does this URL do: {api_url}? Answer in 1 short line."
                            try:
                                ai_ans = requests.get(ask_ai_url, timeout=15).text
                                url_desc = ai_ans.strip()
                            except: pass
                        
                        file_name = f"{letter}1_{category}_url.py"
                        file_path = os.path.join(folder_path, file_name)
                        
                        code = f"""import sys, os, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from service_api.integrations.telegram_helper import send_telegram_message
def run_test():
    res = requests.get("{api_url}", timeout=15)
    send_telegram_message(f"✅ Verified ({category}): Status {{res.status_code}}")
if __name__ == "__main__": run_test()
"""
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(code)
                        
                        used_urls.add(api_url)
                        print(f"✅ SUCCESS: Saved to {letter}/{file_name}")
                        
                        # 🔥 TELEGRAM MESSAGE WITH DETAILS 🔥
                        if token and chat_id:
                            msg = f"✅ <b>[{letter}] NEW API URL</b>\n"
                            msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                            msg += f"🔗 <b>URL:</b> <code>{api_url}</code>\n"
                            if url_title: msg += f"📌 <b>Title:</b> {url_title}\n"
                            if url_desc: msg += f"📝 <b>Details:</b> {url_desc}\n"
                            msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                            msg += f"📂 <b>Folder:</b> {letter}/{file_name}"
                            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
                            
                except Exception as e:
                    print(f"⚠️ Error: {e}")
    except Exception as e:
        print(f"❌ AI Error: {e}")
        
    time.sleep(2)

print("\n🎉 Done!")
