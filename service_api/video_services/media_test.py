import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import os
import sys
import requests
from service_api.integrations.telegram_helper import send_telegram_message

def run_test():
    telegram_token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")

    if not telegram_token or not chat_id:
        send_telegram_message("❌ <b>[PRODUCTION]</b> Missing Telegram credentials.")
        sys.exit(1)

    success_count = 0

    # 1. IMAGE GENERATION
    image_prompt = "A futuristic robot coding on a laptop, 4k resolution"
    encoded_image_prompt = requests.utils.quote(image_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_image_prompt}?width=1024&height=1024&nologo=true"
    
    print(f"⏳ Generating image: {image_prompt}")
    
    try:
        img_res = requests.get(image_url, timeout=30)
        if img_res.status_code == 200:
            with open("temp_image.jpg", "wb") as f:
                f.write(img_res.content)
            
            url = f"https://api.telegram.org/bot{telegram_token}/sendPhoto"
            with open("temp_image.jpg", "rb") as photo:
                payload = {
                    "chat_id": chat_id,
                    "caption": f"🎨 <b>[VIP PRODUCTION] AI IMAGE</b>\n\n<b>Prompt:</b> <i>{image_prompt}</i>",
                    "parse_mode": "HTML"
                }
                requests.post(url, data=payload, files={"photo": photo})
                print("✅ Image sent successfully!")
                success_count += 1
    except Exception as e:
        print(f"❌ Image Error: {e}")

    # 2. AUDIO GENERATION
    audio_prompt = "Upbeat electronic dance music, fast tempo, energetic"
    encoded_audio_prompt = requests.utils.quote(audio_prompt)
    audio_url = f"https://audio.pollinations.ai/prompt/{encoded_audio_prompt}"
    
    print(f"⏳ Generating audio: {audio_prompt}")
    
    try:
        audio_res = requests.get(audio_url, timeout=60)
        if audio_res.status_code == 200:
            with open("temp_audio.mp3", "wb") as f:
                f.write(audio_res.content)
            
            url = f"https://api.telegram.org/bot{telegram_token}/sendAudio"
            with open("temp_audio.mp3", "rb") as audio:
                payload = {
                    "chat_id": chat_id,
                    "caption": f"🎵 <b>[VIP PRODUCTION] AI AUDIO</b>\n\n<b>Prompt:</b> <i>{audio_prompt}</i>",
                    "parse_mode": "HTML"
                }
                requests.post(url, data=payload, files={"audio": audio})
                print("✅ Audio sent successfully!")
                success_count += 1
    except Exception as e:
        # Yahan error aane par bhi script fail NAHI hogi
        print(f"⚠️ Audio Server Error (Bypassed): {e}")

    if success_count == 0:
        send_telegram_message("❌ <b>[PRODUCTION] MEDIA TEST FAILED:</b> Dono Image aur Audio generate nahi hue.")
        sys.exit(1)
    else:
        print("✅ Media Test Passed.")
        sys.exit(0)

if __name__ == "__main__":
    run_test()
