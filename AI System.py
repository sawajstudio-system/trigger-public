import os
import requests
import time

print("🚀 Auto-Add 26 Folders System Started...")

base_dir = "service_url"
os.makedirs(base_dir, exist_ok=True)

# Ab hum ek Loop chalayenge (Z tak)
for i in range(26):
    letter = chr(65 + i) # A, B, C... Z
    folder_path = os.path.join(base_dir, letter)
    os.makedirs(folder_path, exist_ok=True)
    
    print(f"\n🔍 [{letter}] Asking AI for new URL...")
    
    # AI se naya URL mangwa rahe hain
    prompt = f"Give me 1 real, working open-source API URL for category related to {letter}. Format strictly: Category|URL. Do not add text."
    url = f"https://text.pollinations.ai/{requests.utils.quote(prompt)}"
    
    try:
        res = requests.get(url, timeout=60)
        ai_response = res.text
        
        # AI ke response ko parse karna
        if '|' in ai_response:
            parts = ai_response.split('|')
            category = parts[0].strip().replace(' ', '_').lower()
            api_url = parts[1].strip()
            
            # Check if URL is valid
            if api_url.startswith("http"):
                # 🔥 LIVE CHECK 🔥
                try:
                    test = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    if test.status_code in [200, 201, 202]:
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
                        
                        print(f"✅ Added to {letter}: {file_name}")
                    else:
                        print(f"❌ URL Failed: {api_url}")
                except Exception:
                    print(f"❌ Network Error: {api_url}")
    except Exception as e:
        print(f"❌ AI Error: {e}")
    
    time.sleep(2) # 2 second ruko

print("\n🎉 All 26 Folders A-Z Created with Automatic URLs!")
