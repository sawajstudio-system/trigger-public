import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Folder: API
# File: pexels_test.py
import os
import sys
import requests
from service_api.integrations.telegram_helper import send_telegram_message

def run_test():
    api_key = os.getenv("PEXELS_API_KEY")
    telegram_token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not api_key:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Pexels test failed: PEXELS_API_KEY missing.")
        sys.exit(1)

    search_query = "coding"
    headers = {"Authorization": api_key}
    api_url = f"https://api.pexels.com/videos/search?query={search_query}&per_page=1"

    try:
        res = requests.get(api_url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data.get("videos"):
                video_data = data["videos"][0]
                # Best quality video link nikalna
                video_files = video_data.get("video_files", [])
                if video_files:
                    video_files.sort(key=lambda x: x.get("width", 0), reverse=True)
                    video_link = video_files[0]["link"]
                    
                    tg_url = f"https://api.telegram.org/bot{telegram_token}/sendVideo"
                    payload = {
                        "chat_id": chat_id,
                        "video": video_link,
                        "caption": f"🎬 <b>[VIP PRODUCTION] PEXELS VIDEO</b>\n\n<b>Query:</b> <i>{search_query}</i>\n\n🚀 <i>Powered by Pexels</i>",
                        "parse_mode": "HTML"
                    }
                    requests.post(tg_url, data=payload)
                    print("✅ Pexels Video sent!")
                else:
                    send_telegram_message("❌ <b>[PRODUCTION]</b> Pexels: No video files found.")
                    sys.exit(1)
            else:
                send_telegram_message("❌ <b>[PRODUCTION]</b> Pexels: No video found.")
                sys.exit(1)
        else:
            send_telegram_message(f"❌ <b>[PRODUCTION]</b> Pexels failed. HTTP {res.status_code}")
            sys.exit(1)
    except Exception as e:
        send_telegram_message(f"❌ <b>[PRODUCTION]</b> Pexels Network Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_test()
