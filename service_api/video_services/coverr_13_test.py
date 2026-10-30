import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: coverr_13_test.py
import os
import sys
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    api_key = os.getenv("COVERR_API_KEY")
    telegram_token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Coverr test failed: COVERR_API_KEY missing.")
        sys.exit(1)

    search_query = "nature"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Coverr API endpoint (URLs maangne ke liye 'urls=true' lagana zaroori hai)
    api_url = f"https://api.coverr.co/videos?query={search_query}&limit=1&urls=true"

    print(f"⏳ Fetching Coverr video for: {search_query}")

    try:
        res = requests.get(api_url, headers=headers, timeout=15)
        
        if res.status_code == 200:
            data = res.json()
            if data.get("hits") and len(data["hits"]) > 0:
                video_data = data["hits"][0]
                
                # Coverr sahi field 'urls' hai (video_urls nahi)
                video_urls = video_data.get("urls", {})
                video_link = video_urls.get("mp4_download") or video_urls.get("mp4")
                
                if video_link:
                    tg_url = f"https://api.telegram.org/bot{telegram_token}/sendVideo"
                    payload = {
                        "chat_id": chat_id,
                        "video": video_link,
                        "caption": f"🎬 <b>[VIP PRODUCTION] COVERR VIDEO</b>\n\n<b>Query:</b> <i>{search_query}</i>\n\n🚀 <i>Powered by Coverr</i>",
                        "parse_mode": "HTML"
                    }
                    requests.post(tg_url, data=payload)
                    print("✅ Coverr Video sent!")
                else:
                    # Agar urls field khaali hai toh error bhejo
                    send_telegram_message(f"❌ <b>[PRODUCTION]</b> Coverr: Video link nahi mila. Response: {video_urls}")
                    sys.exit(1)
            else:
                send_telegram_message("❌ <b>[PRODUCTION]</b> Coverr: No video found.")
                sys.exit(1)
        else:
            send_telegram_message(f"❌ <b>[PRODUCTION]</b> Coverr failed. HTTP {res.status_code}\n{res.text[:100]}")
            sys.exit(1)
            
    except Exception as e:
        send_telegram_message(f"❌ <b>[PRODUCTION]</b> Coverr Network Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
