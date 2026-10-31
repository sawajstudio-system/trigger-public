import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: tanvo_test.py
import os
import sys
import time
import requests
from service_api.integrations.telegram_helper import send_telegram_message

def run_test():
    api_key = os.getenv("TANVO_API_KEY")
    telegram_token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Tanvo test failed: TANVO_API_KEY missing.")
        sys.exit(1)

    api_url = "https://tanvo.ai/api/v1/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 🛠️ DOCUMENTATION KE MUTABIQ EXACT PARAMETERS
    payload = {
        "model": "nano-banana-2",
        "prompt": "A futuristic cyberpunk city at night",
        "kind": "image",
        "options": {
            "resolution": "2K"
        }
    }

    print("⏳ Requesting image from Tanvo AI (Confirmed)...")

    try:
        res = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if res.status_code in [200, 201, 202]:
            data = res.json()
            run_id = data.get("id") or data.get("run_id")
            
            if not run_id:
                send_telegram_message(f"❌ <b>[PRODUCTION]</b> Tanvo: Run ID nahi mila.\n{str(data)[:100]}")
                sys.exit(1)
                
            print(f"✅ Request accepted. Run ID: {run_id}")
            
            max_attempts = 20
            image_url = None
            
            for attempt in range(max_attempts):
                time.sleep(5)
                status_url = f"{api_url}/{run_id}"
                status_res = requests.get(status_url, headers=headers, timeout=15)
                
                if status_res.status_code == 200:
                    status_data = status_res.json()
                    status = status_data.get("status")
                    
                    print(f"🔄 Attempt {attempt + 1}: Status = {status}")
                    
                    if status == "completed" or status == "success":
                        output = status_data.get("output", {})
                        # Documentation ke mutabiq output.images[0].url
                        images = output.get("images", [])
                        if images and len(images) > 0:
                            image_url = images[0].get("url")
                        break
                    elif status == "failed":
                        send_telegram_message(f"❌ <b>[PRODUCTION]</b> Tanvo generation failed.")
                        sys.exit(1)
            
            if image_url:
                tg_url = f"https://api.telegram.org/bot{telegram_token}/sendPhoto"
                payload_tg = {
                    "chat_id": chat_id,
                    "photo": image_url,
                    "caption": f"🪄 <b>[VIP PRODUCTION] TANVO AI IMAGE</b>\n\n<b>Prompt:</b> <i>{payload['prompt']}</i>\n\n🚀 <i>Powered by Tanvo AI</i>",
                    "parse_mode": "HTML"
                }
                requests.post(tg_url, data=payload_tg)
                print("✅ Tanvo Image sent!")
            else:
                send_telegram_message("❌ <b>[PRODUCTION]</b> Tanvo: Image URL nahi mila (Timeout).")
                sys.exit(1)
                
        else:
            send_telegram_message(f"❌ <b>[PRODUCTION]</b> Tanvo failed. HTTP {res.status_code}\n{res.text[:150]}")
            sys.exit(1)
            
    except Exception as e:
        send_telegram_message(f"❌ <b>[PRODUCTION]</b> Tanvo Network Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
