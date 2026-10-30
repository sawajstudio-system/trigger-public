# Folder: API
# File: pixabay_11_test.py
import os
import sys
import requests
from service_api.integrations.telegram_01_helper import send_telegram_message

def run_test():
    api_key = os.getenv("PIXABAY_API_KEY")
    telegram_token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not api_key or not telegram_token or not chat_id:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Missing Credentials.")
        sys.exit(1)

    # Aap yahan apna keyword change kar sakte hain
    search_query = "nature"
    
    # 1. VIDEO FETCH KARNA
    print(f"⏳ Fetching video for: {search_query}")
    video_url = f"https://pixabay.com/api/videos/?key={api_key}&q={search_query}&per_page=3"
    
    try:
        res = requests.get(video_url, timeout=15)
        data = res.json()
        
        if data.get("hits"):
            # Pehla video uthate hain
            video_data = data["hits"][0]
            video_link = video_data["videos"]["medium"]["url"]
            
            # Video Telegram par bhejna (URL se direct)
            tg_url = f"https://api.telegram.org/bot{telegram_token}/sendVideo"
            payload = {
                "chat_id": chat_id,
                "video": video_link,
                "caption": f"🎬 <b>[VIP PRODUCTION] STOCK VIDEO</b>\n\n<b>Query:</b> <i>{search_query}</i>\n\n🚀 <i>Powered by Pixabay</i>",
                "parse_mode": "HTML"
            }
            requests.post(tg_url, data=payload)
            print("✅ Video sent!")
        else:
            print("❌ No video found.")
            
    except Exception as e:
        print(f"❌ Video Error: {e}")

    # 2. MUSIC (AUDIO) FETCH KARNA
    print(f"⏳ Fetching music for: {search_query}")
    # Pixabay music API thoda alag endpoint use karta hai
    music_url = f"https://pixabay.com/api/?key={api_key}&q={search_query}&category=music&per_page=3"
    
    try:
        res_music = requests.get(music_url, timeout=15)
        data_music = res_music.json()
        
        if data_music.get("hits"):
            music_link = data_music["hits"][0]["previewURL"]
            
            tg_url = f"https://api.telegram.org/bot{telegram_token}/sendAudio"
            payload = {
                "chat_id": chat_id,
                "audio": music_link,
                "caption": f"🎵 <b>[VIP PRODUCTION] BACKGROUND MUSIC</b>\n\n<b>Query:</b> <i>{search_query}</i>\n\n🚀 <i>Powered by Pixabay</i>",
                "parse_mode": "HTML"
            }
            requests.post(tg_url, data=payload)
            print("✅ Audio sent!")
        else:
            print("❌ No music found.")
            
    except Exception as e:
        print(f"❌ Music Error: {e}")

if __name__ == "__main__":
    run_test()
