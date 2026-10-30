import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: magic_test.py
import os
import sys
import time
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    api_key = os.getenv("MAGICHOUR_API_KEY")
    telegram_token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Magic Hour failed: MAGICHOUR_API_KEY missing.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = "A futuristic robot coding on a laptop, 4k resolution"
    
    # Step 1: Image Generate karne ki request bhejna
    payload = {
        "name": "VIP Production Image",
        "image_count": 1,
        "model": "z-image-turbo",
        "aspect_ratio": "16:9",
        "resolution": "640px",
        "style": {
            "prompt": prompt,
            "tool": "ai-anime-generator"  # Aap yahan style change kar sakte hain
        }
    }
    
    print(f"⏳ Requesting Magic Hour for image: {prompt}")
    
    try:
        res = requests.post("https://api.magichour.ai/v1/ai-image-generator", headers=headers, json=payload, timeout=30)
        
        if res.status_code in [200, 201]:
            data = res.json()
            project_id = data.get("id")
            
            if not project_id:
                send_telegram_message(f"❌ <b>[PRODUCTION]</b> Magic Hour: Project ID nahi mila.\n{str(data)[:100]}")
                sys.exit(1)
                
            print(f"✅ Request accepted. Project ID: {project_id}")
            print("⏳ Waiting for image to generate...")
            
            # Step 2: Polling Loop (Har 5 second mein check karna)
            max_attempts = 20  # 20 * 5 = 100 seconds tak wait karega
            image_url = None
            
            for attempt in range(max_attempts):
                time.sleep(5)  # 5 second wait
                
                # Project status check karna
                status_url = f"https://api.magichour.ai/v1/image-projects/{project_id}"
                status_res = requests.get(status_url, headers=headers, timeout=15)
                
                if status_res.status_code == 200:
                    status_data = status_res.json()
                    status = status_data.get("status")
                    
                    print(f"🔄 Attempt {attempt + 1}: Status = {status}")
                    
                    if status == "complete":
                        # Image ban gayi! Download URL nikalna
                        downloads = status_data.get("downloads", [])
                        if downloads and len(downloads) > 0:
                            image_url = downloads[0].get("url")
                            break
                    elif status == "error":
                        send_telegram_message(f"❌ <b>[PRODUCTION]</b> Magic Hour Error: Image generation failed.")
                        sys.exit(1)
                else:
                    print(f"⚠️ Status check failed: HTTP {status_res.status_code}")
            
            # Step 3: Image Telegram par bhejna
            if image_url:
                tg_url = f"https://api.telegram.org/bot{telegram_token}/sendPhoto"
                payload_tg = {
                    "chat_id": chat_id,
                    "photo": image_url,
                    "caption": f"🎨 <b>[VIP PRODUCTION] MAGIC HOUR IMAGE</b>\n\n<b>Prompt:</b> <i>{prompt}</i>\n\n🚀 <i>Powered by Magic Hour</i>",
                    "parse_mode": "HTML"
                }
                requests.post(tg_url, data=payload_tg)
                print("✅ Magic Hour Image sent!")
            else:
                send_telegram_message("❌ <b>[PRODUCTION]</b> Magic Hour: Image generate nahi hui (Timeout).")
                sys.exit(1)
                
        else:
            send_telegram_message(f"❌ <b>[PRODUCTION]</b> Magic Hour failed. HTTP {res.status_code}\n{res.text[:150]}")
            sys.exit(1)
            
    except Exception as e:
        send_telegram_message(f"❌ <b>[PRODUCTION]</b> Magic Hour Network Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
