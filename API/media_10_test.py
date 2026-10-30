# Folder: API
# File: media_10_test.py
import os
import sys
import requests
from telegram_01_helper import send_telegram_message

def run_test():
    telegram_token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not telegram_token or not chat_id:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Missing Telegram credentials.")
        sys.exit(1)

    # ==========================================
    # 1. IMAGE GENERATION
    # ==========================================
    image_prompt = "A futuristic robot coding on a laptop, 4k resolution"
    encoded_image_prompt = requests.utils.quote(image_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_image_prompt}?width=1024&height=1024&nologo=true"
    
    print(f"⏳ Generating image: {image_prompt}")
    
    try:
        img_res = requests.get(image_url, timeout=30)
        if img_res.status_code == 200:
            with open("temp_image.jpg", "wb") as f:
                f.write(img_res.content)
            
            # Telegram par Image bhejna
            url = f"https://api.telegram.org/bot{telegram_token}/sendPhoto"
            with open("temp_image.jpg", "rb") as photo:
                payload = {
                    "chat_id": chat_id,
                    "caption": f"🎨 <b>[VIP PRODUCTION] AI IMAGE</b>\n\n<b>Prompt:</b> <i>{image_prompt}</i>",
                    "parse_mode": "HTML"
                }
                requests.post(url, data=payload, files={"photo": photo})
                print("✅ Image sent successfully!")
        else:
            print(f"❌ Image generation failed. HTTP {img_res.status_code}")
    except Exception as e:
        print(f"❌ Image Error: {e}")

    # ==========================================
    # 2. AUDIO GENERATION (Song)
    # ==========================================
    audio_prompt = "Upbeat electronic dance music, fast tempo, energetic"
    encoded_audio_prompt = requests.utils.quote(audio_prompt)
    audio_url = f"https://audio.pollinations.ai/prompt/{encoded_audio_prompt}"
    
    print(f"⏳ Generating audio: {audio_prompt}")
    
    try:
        audio_res = requests.get(audio_url, timeout=60)
        if audio_res.status_code == 200:
            with open("temp_audio.mp3", "wb") as f:
                f.write(audio_res.content)
            
            # Telegram par Audio bhejna
            url = f"https://api.telegram.org/bot{telegram_token}/sendAudio"
            with open("temp_audio.mp3", "rb") as audio:
                payload = {
                    "chat_id": chat_id,
                    "caption": f"🎵 <b>[VIP PRODUCTION] AI AUDIO</b>\n\n<b>Prompt:</b> <i>{audio_prompt}</i>",
                    "parse_mode": "HTML"
                }
                requests.post(url, data=payload, files={"audio": audio})
                print("✅ Audio sent successfully!")
        else:
            print(f"❌ Audio generation failed. HTTP {audio_res.status_code}")
    except Exception as e:
        print(f"❌ Audio Error: {e}")

if __name__ == "__main__":
    run_test()
